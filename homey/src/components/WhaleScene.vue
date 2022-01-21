<template>
  <div id="whale-canvas" ref="threeCanvas">
    <div ref="tooltip" id="tooltip">{{tooltipText}}</div>
  </div>
</template>

<script>
import * as THREE from 'three';   // TODO: selective import
import * as TWEEN from '@tweenjs/tween.js'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry';

// define three.js objects outside of vue export
// to avoid making them reactive
const scene = new THREE.Scene();
const raycaster = new THREE.Raycaster();
const light = new THREE.DirectionalLight(0xffffff);
const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    100
);

// orthographic camera
// let width = window.innerWidth
// let height = window.innerHeight
// const camera = new THREE.OrthographicCamera( width / - 2, width / 2, height / 2, height / - 2, 1, 100 );

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
const controls = new OrbitControls(camera, renderer.domElement);

const clippingPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -.34);
const invisMat = new THREE.MeshPhongMaterial({side: THREE.FrontSide, color: 0x000000, visible: false});

const gltfLoader = new GLTFLoader();
const imgLoader = new THREE.TextureLoader();

// load whale once (not on every component load)
gltfLoader.load('./models/docker.glb', (model) => { 
  model.scene.position.y -= .75; 
  scene.add(model.scene); 
});

let mousePos = new THREE.Vector2(100, 100);
let boundingBoxes = [];
let uiColor = 0x00a7ff;
let hoveredButton;

export default {
    name: 'WhaleScene',
    props: {
      services: Array,
    },
    emits: ['3dClick'],
    components: {
    },
    watch: {
      services: {
        handler: function() {
          this.updateCrates();
        },
        deep: true,
      },
    },
    data: function() {
        return {
            serviceData: [],
            crates: [],
            tooltipText: '',
            animationFinished: false,
        };
    },
    // scene setup
    created: function() {
        this.serviceData = this.services;

        // spawn a crate for each service
        this.serviceData.forEach(s => { this.addCrate(s.name); });

        // for bounding boxes
        raycaster.layers.set(1);

        // lights & camera
        scene.add(light);
        scene.add(camera);
        light.position.set(-5, 3, 2);
        camera.position.set(-.25, 1, 8);

        // initial camera transition animation
        const camSpawnTween = new TWEEN.Tween(camera).to({
          position: { x: -6, y: 2, z: 4 },
        }, 4000)
        .easing(TWEEN.Easing.Sinusoidal.InOut)
        .delay(1000)
        .onStart(() => { this.animationFinished = false; })
        //.onUpdate(() => { camera.updateProjectionMatrix() })  // ortho camera swap
        .onComplete(() => { this.animationFinished = true; })
        .start();
        
        renderer.setPixelRatio( window.devicePixelRatio );
        renderer.localClippingEnabled = true;

        this.initControls();
    },
    // add canvas & begin animation loop
    mounted: function() {
        this.$refs.threeCanvas.appendChild(renderer.domElement)

        // ortho camera swap
        // let width = this.$refs.threeCanvas.clientWidth
        // let height =this.$refs.threeCanvas.clientHeight
        // camera.left = width / - 100
        // camera.right = width / 100
        // camera.top = height / 100
        // camera.bottom = height / - 100
        // camera.updateProjectionMatrix();

        this.$refs.threeCanvas.addEventListener('mousemove', this.onMouseMove, false );
        this.$refs.threeCanvas.addEventListener('mousedown', this.onMouseDown, false );
        
        this.animate()
    },
    methods: {
        // main loop
        animate: function() {
            if(!this.$refs.threeCanvas) return;
            
            let width = this.$refs.threeCanvas.clientWidth;
            let height = this.$refs.threeCanvas.clientHeight;

            if(camera.aspect != width / height) this.updateCameraAspect(width, height);

            TWEEN.update();
            controls.update();
            
            // raycasting moved to onMouseMove for efficiency

            renderer.setSize(width, height);
            requestAnimationFrame(this.animate)
            
            renderer.render(scene, camera); 
        },  
        // detect crate and button mouseover events
        raycast() {
          raycaster.setFromCamera(mousePos, camera);
          
          // detect mouseover events on crates
          const intersects = raycaster.intersectObjects(boundingBoxes);
          if(intersects.length > 0) {
            // intersects[0] is hovered crate's bounding box 
            let hitCrate = intersects[0].object.parent;

            // if crate is expanded enough...
            if(hitCrate.userData.box.position.z > 1.4) {
              // ...detect mouseover events on its buttons
              const uiCast = raycaster.intersectObjects(hitCrate.userData.UI.children);
              // if a button is hovered
              if (uiCast.length > 0) {
                // reset last hovered button color
                if(hoveredButton) hoveredButton.material.emissive.set(uiColor)  
                // set hovered button to selected color
                hoveredButton = uiCast[0].object;                               
                hoveredButton.material.emissive.set(0x000000);             
              }
              // if no button is hovered
              else {
                // reset all button colors
                hitCrate.userData.UI.children.forEach(btn => {
                  if(btn.material.emissive) btn.material.emissive.set(uiColor)
                });
                hoveredButton = null;
              }
            }

            // if crate is already expanding or expanded, do nothing
            if(hitCrate.userData.box.scale.z > 1.05)  return;
            // otherwise expand selected crate and shrink all others
            this.shrinkAll(hitCrate);
          }
          // if no raycast hit...
          else{
            // ...shrink any expanded crates
            this.shrinkAll();
            // and reset tooltip
            hoveredButton = null;
          }
        },
        // update camera to canvas size
        updateCameraAspect(width, height){
          camera.aspect = width / height;
          camera.updateProjectionMatrix();
        },
        // update bounding boxes to parent positions
        updateBoundingBoxes(){
          boundingBoxes.forEach( b => {
            let box = b.parent.userData.box;
            if(box.scale.z > 1.05) {
              b.scale.z = box.scale.z;
              b.position.z = box.position.z;
            }
          });
        },
        // shrinks all crates except specified
        shrinkAll(exceptCrate){
          if(exceptCrate) {
            this.growCrate(exceptCrate);
          }

          this.crates.forEach(c => {
            if(exceptCrate) {
              if(c.name != exceptCrate.name)  this.shrinkCrate(c);
            }
            else this.shrinkCrate(c);
          });
        },
        // elastic pop out animation
        growCrate(crateObj){
          if(crateObj.userData.box.scale.z > 1.05) return;

          if(crateObj.userData.animation) TWEEN.remove(crateObj.userData.animation);
          crateObj.userData.animation = new TWEEN.Tween(crateObj)
            .to({ userData: {
                box: {
                  scale: {z: (crateObj.userData.textSize.max.z - crateObj.userData.textSize.min.z) + .4 * 6 },   // title + button panel width
                  position: {z:(-1 + (crateObj.userData.textSize.max.z - crateObj.userData.textSize.min.z) + .4 * 6 ) / 2}
                },
                UI: {
                  position: {z: .25 + (crateObj.userData.textSize.max.z - crateObj.userData.textSize.min.z) + .4 * 6 }
                }
             }}, 1600) 
            .easing(TWEEN.Easing.Elastic.Out)
            .onUpdate(this.updateBoundingBoxes)
            .start();
        },
        // smooth shrink animation
        shrinkCrate(crateObj){
          if(crateObj.userData.box.scale.z < 1.05) return;

          if(crateObj.userData.animation) TWEEN.remove(crateObj.userData.animation);
          // crateObj.userData.animation = new TWEEN.Tween(crateObj.userData.box)
          //   .to({ scale: {x: 1, z: 1, y: 1}, position: {z: 0} }, 600)
          crateObj.userData.animation = new TWEEN.Tween(crateObj)
            .to({ userData: {
                box: {
                  scale: {x: 1, z: 1, y: 1}, 
                  position: {z: 0},
                },
                UI: {
                  position: {z: -2 + (crateObj.userData.textSize.max.z - crateObj.userData.textSize.min.z) / 2 - (.4 * 6) },
                }
             }}, 600)
            .easing(TWEEN.Easing.Quadratic.Out)
            .onUpdate(this.updateBoundingBoxes)
            .start();
        },
        // new crate from service name
        addCrate(serviceName) {
          let grp = new THREE.Group();
          grp.name = serviceName;
          grp.position.x += ((this.crates.length % 5) * 1.1) - 2.9;
          grp.position.y += Math.floor(this.crates.length / 5)

          // rounded box
          const boxMat = new THREE.MeshPhongMaterial({
              side: THREE.FrontSide,
              color: 0xf8f8f8,
          });
          let box = new THREE.Mesh(new RoundedBoxGeometry(1, 1, 1, 6, .1), boxMat);
          grp.add(box);

          let uiGrp = new THREE.Group();
          let btnSize = .4;
          const buttonGeo = new THREE.PlaneGeometry(btnSize, btnSize);

          // service name
          let text = this.TextToMesh(serviceName, .35, 1, 80, uiColor);
          text.rotateY(Math.PI * 1.5);
          text.position.x -= 0.02;
          
          let textSize = new THREE.Box3().setFromObject(text);
          text.position.x -= .5;
          text.position.y -= .02;
          text.position.z -= ((textSize.max.z - textSize.min.z) / 2 + (btnSize * 6)) 
          textSize.setFromObject(text);
          uiGrp.add(text);

          // buttons
          let btnStartMat = new THREE.MeshPhongMaterial({
              side: THREE.FrontSide,
              map: imgLoader.load('./images/ui/start.png'),
              transparent: true,
              emissive: uiColor,
              clippingPlanes: [clippingPlane],
              clipIntersection: true
          });
          const btnStart = new THREE.Mesh(buttonGeo, btnStartMat);
          btnStart.rotateY(Math.PI * 1.5);
          btnStart.position.x = text.position.x - .02;
          btnStart.position.z = textSize.max.z + (btnSize / 4);
          btnStart.layers.enable(1);
          btnStart.name = 'start'
          uiGrp.add(btnStart);

          let btnStopMat = new THREE.MeshPhongMaterial({
              side: THREE.FrontSide,
              map: imgLoader.load('./images/ui/stop.png'),
              transparent: true,
              emissive: uiColor,
              clippingPlanes: [clippingPlane],
              clipIntersection: true
          });
          const btnStop = new THREE.Mesh(buttonGeo, btnStopMat);
          btnStop.rotateY(Math.PI * 1.5);
          btnStop.position.x = text.position.x - .02;
          btnStop.position.z = btnStart.position.z + btnSize;
          btnStop.layers.enable(1);
          btnStop.name = 'stop'
          uiGrp.add(btnStop);

          let btnRestartMat = new THREE.MeshPhongMaterial({
              side: THREE.FrontSide,
              map: imgLoader.load('./images/ui/restart.png'),
              transparent: true,
              emissive: uiColor,
              clippingPlanes: [clippingPlane],
              clipIntersection: true
          });
          const btnRestart = new THREE.Mesh(buttonGeo, btnRestartMat);
          btnRestart.rotateY(Math.PI * 1.5);
          btnRestart.position.x = text.position.x - .02;
          btnRestart.position.z = btnStop.position.z + btnSize;
          btnRestart.layers.enable(1);
          btnRestart.name = 'restart'
          uiGrp.add(btnRestart);

          let btnInfoMat = new THREE.MeshPhongMaterial({
              side: THREE.FrontSide,
              map: imgLoader.load('./images/ui/info.png'),
              transparent: true,
              emissive: uiColor,
              clippingPlanes: [clippingPlane],
              clipIntersection: true
          });
          const btnInfo = new THREE.Mesh(buttonGeo, btnInfoMat);
          btnInfo.rotateY(Math.PI * 1.5);
          btnInfo.position.x = text.position.x - .02;
          btnInfo.position.z = btnRestart.position.z + btnSize;
          btnInfo.layers.enable(1);
          btnInfo.name = 'info'
          uiGrp.add(btnInfo);

          grp.add(uiGrp);

          // service image
          let serviceImgMat = new THREE.MeshPhongMaterial({
              side: THREE.FrontSide,
              map: imgLoader.load('./images/icons/' + serviceName + '.png'),
              transparent: true,
          });
          const serviceImg = new THREE.Mesh(buttonGeo, serviceImgMat);
          serviceImg.position.z += .502;
          serviceImg.scale.set(1.5, 1.5, 1)
          grp.add(serviceImg);
          serviceImg.parent = box;

          const serviceImgHidden = new THREE.Mesh(buttonGeo, serviceImgMat);
          serviceImgHidden.position.x -= .502;
          serviceImgHidden.scale.set(1.5, 1.5, 1)
          serviceImgHidden.rotateY(Math.PI * 1.5);
          
          grp.add(serviceImgHidden);

          // bounding box
          let bbox = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), invisMat);
          bbox.name = grp.name + '_bbox';
          bbox.layers.enable(1);
          scene.add(bbox);
          bbox.parent = grp;
          boundingBoxes.push(bbox);

          grp.userData = { 
            animation: null,
            box: box,
            UI: uiGrp,
            textSize: textSize
          };

          // elastic spawn animation          
          grp.scale.set(0,0,0)
          let tScale = new TWEEN.Tween(grp.scale)
            .to({x: 1, y: 1, z: 1}, (Math.random() + 1) * 1500)   // slightly random stagger
            .easing(TWEEN.Easing.Elastic.Out)
            .delay(this.crates.length * 175)
          tScale.start();

          this.crates.push(grp);
          scene.add(grp);
        },
        // remove existing crate
        removeCrate(crateObj) {
          boundingBoxes.splice(boundingBoxes.findIndex(b => b.name == crateObj.name + '_bbox'), 1);
          this.crates.splice(this.crates.indexOf(crateObj), 1);

          //elastic despawn animation
          const tScale = new TWEEN.Tween(crateObj.scale)
            .to({x: 0, y: 0, z: 0}, 750)
            .easing(TWEEN.Easing.Elastic.In)
            .onComplete(() => {
              scene.remove(scene.getObjectByName(crateObj.name + '_bbox'));
              scene.remove(scene.getObjectByName(crateObj.name));
            })
          tScale.start()
        },
        // triggered on services array change
        updateCrates() {
          // add crates for newly added services
          this.serviceData.forEach(s => {
            let found = false;
            this.crates.forEach(c => { if(s.name == c.name) found = true; })
            if(!found) this.addCrate(s.name);
          });
          // remove crates for deleted services
          this.crates.forEach(c => {
            let found = false;
            this.serviceData.forEach(s => { if(s.name == c.name) found = true; })
            if (!found) this.removeCrate(c);
          })
        },
        // camera settings
        initControls(){
          // limit movement
          controls.maxAzimuthAngle = 0 + 0.2;  
          controls.minAzimuthAngle = Math.PI / -2 - 0.2;
          controls.maxPolarAngle = Math.PI / 2 + 0.2;
          controls.minPolarAngle = Math.PI / 4;
          controls.minDistance = 3;
          controls.maxDistance = 15;
          controls.enablePan = false;
          // sense of inertia
          controls.enableDamping = true;
          controls.dampingFactor = .02;
        },
        // UI click event
        onMouseDown(event) {
          if(!hoveredButton)  return;
          // emit 3dClick(serviceName, operation)
          this.$emit('3dClick', hoveredButton.parent.parent.name, hoveredButton.name)
        },
        // keep track of mouse position (normalized to [-1, 1])
        onMouseMove(event) {
          mousePos.x = ( (event.offsetX / this.$refs.threeCanvas.clientWidth)  ) * 2 - 1;
          mousePos.y = - ( (event.offsetY / this.$refs.threeCanvas.clientHeight) ) * 2 + 1;

          // do not raycast if initial camera transition is playing
          if(this.animationFinished)  this.raycast();     
          this.updateTooltip(event);
        },
        updateTooltip(event){
          if (!hoveredButton) {
            this.$refs.tooltip.style.opacity = 0;
            return;
          }
          this.$refs.tooltip.style.opacity = 1;
          this.tooltipText = hoveredButton.name[0].toUpperCase() + hoveredButton.name.substring(1) + ' ' + hoveredButton.parent.parent.name;
          this.$refs.tooltip.style.left = event.offsetX + 'px';
          this.$refs.tooltip.style.top = event.offsetY -25 + 'px';
        },
        // returns a transparent plane with specified text drawn
        // credit to dcromley: https://discourse.threejs.org/t/13757
        TextToMesh(txt, hWorldTxt, hWorldAll, hPxTxt, color, sprite=false) {
          let kPxToWorld = hWorldTxt/hPxTxt;                // px to world multplication factor
          let hPxAll = Math.ceil(hWorldAll/kPxToWorld);     // height of the whole texture canvas

          // create the canvas for the texture
          let txtcanvas = document.createElement("canvas");
          let ctx = txtcanvas.getContext("2d");
          ctx.font = hPxTxt + "px sans-serif";   

          // get all widths
          let wPxTxt = ctx.measureText(txt).width;         // wPxTxt: width of the text in the texture canvas
          let wWorldTxt = wPxTxt*kPxToWorld;               // wWorldTxt: world width of text in the plane
          let wWorldAll = wWorldTxt+(hWorldAll-hWorldTxt); // wWorldAll: world width of the whole plane
          let wPxAll = Math.ceil(wWorldAll/kPxToWorld);    // wPxAll: width of the whole texture canvas
          
          // resize the texture canvas
          txtcanvas.width =  wPxAll;
          txtcanvas.height = hPxAll;
        
          // fill text
          ctx.textAlign = "center";
          ctx.textBaseline = "middle"; 
          ctx.fillStyle = "#" + color.toString(16)
          ctx.font = hPxTxt + "px sans-serif";   // needed after resize
          ctx.fillText(txt, wPxAll/2, hPxAll/2); 

          // create material + mesh from text
          let material;
          let textTexture = new THREE.CanvasTexture(txtcanvas)
          if(sprite){
            material = new THREE.SpriteMaterial({map: textTexture});
            return new THREE.Sprite(material)
          }
          else{
            material = new THREE.MeshBasicMaterial( { side:THREE.FrontSide, map: textTexture, 
              transparent:true, clippingPlanes: [clippingPlane], clipIntersection: true
            });
            return new THREE.Mesh(new THREE.PlaneGeometry(wWorldAll, hWorldAll), material);
          }
        },
        // destroy scene (triggered on 3D -> 2D swap)
        cleanup() {
          this.crates.forEach(c => {
            scene.remove(scene.getObjectByName(c.name + '_bbox'));
            scene.remove(scene.getObjectByName(c.name));
          });

          boundingBoxes.splice(0, boundingBoxes.length);
          this.crates.splice(0, this.crates.length);
          TWEEN.removeAll();
        },
        // free material & attached textures
        disposeMat(material) {
          material.dispose();

          // dispose of textures
          for (const key of Object.keys(material)) {
            const value = material[key];
            if (value && typeof value === 'object' && 'minFilter' in value)   value.dispose();
          }
        }
    },
}
</script>
