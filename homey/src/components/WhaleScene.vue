<template>
  <div id="three-canvas" ref="threeCanvas"></div>
</template>

<script>
//import { Clock, PerspectiveCamera, Scene, WebGLRenderer } from 'three'
import * as THREE from 'three';
import * as TWEEN from '@tweenjs/tween.js'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { FontLoader } from 'three/examples/jsm/loaders/FontLoader';
import { TextGeometry } from 'three/examples/jsm/geometries/TextGeometry';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry';
import { CSS3DRenderer, CSS3DObject } from 'three/examples/jsm/renderers/CSS3DRenderer';

// define three.js objects outside of vue export
// to avoid making them reactive
const scene = new THREE.Scene();
const raycaster = new THREE.Raycaster();
const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    100
);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.localClippingEnabled = true
const clippingPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), -.34);

const gltfLoader = new GLTFLoader();
const fontLoader = new FontLoader();
const imgLoader = new THREE.TextureLoader();
const light = new THREE.DirectionalLight(0xffffff);
const invisMat = new THREE.MeshPhongMaterial({side: THREE.FrontSide, color: 0x000000, visible: false});

let mousePos = new THREE.Vector2(100, 100);
let boundingBoxes = [];
let uiColor = 0x00a7ff;
let hoveredButton;

const controls = new OrbitControls(camera, renderer.domElement);

export default {
    name: 'WhaleScene',
    props: {
      services: Array,
    },
    emits: ['UI_event'],
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
        };
    },
    // scene setup
    created: function() {
        this.serviceData = this.services;

        // spawn a crate for each service
        this.serviceData.forEach(s => { this.addCrate(s.name); });

        // load whale
        gltfLoader.load('./models/docker.glb', (model) => { 
          model.scene.position.y -= .75; 
          scene.add(model.scene); 
        });

        scene.add(camera)
        scene.add(light)
        light.position.set(-5, 3, 2);
        camera.position.set(-5, 3, 2);
        
        renderer.setPixelRatio( window.devicePixelRatio );
        window.addEventListener('mousemove', this.onMouseMove, false );
        window.addEventListener('mousedown', this.onMouseDown, false );

        // for bounding boxes
        raycaster.layers.set(1);

        // limit camera movement
        controls.maxAzimuthAngle = 0 + 0.2;  
        controls.minAzimuthAngle = Math.PI / -2 - 0.2;
        controls.maxPolarAngle = Math.PI / 2 + 0.2;
        controls.minPolarAngle = Math.PI / 4;
        controls.enablePan = false;
        controls.enableDamping = true;
        controls.dampingFactor = .03;
    },
    // add canvas to page, begin animation loop
    mounted: function() {
        this.$refs.threeCanvas.appendChild(renderer.domElement)
        this.animate()
    },
    computed: {},
    methods: {
        // main loop
        animate: function() {
            TWEEN.update();
            controls.update();

            this.raycast();

            renderer.setSize(window.innerWidth, window.innerHeight);
            requestAnimationFrame(this.animate)
            
            renderer.render(scene, camera);
            
        },
        raycast() {
          raycaster.setFromCamera(mousePos, camera);
          
          // intersects[0] is closest (to camera) hovered crate's bounding box 
          const intersects = raycaster.intersectObjects(boundingBoxes);
          if(intersects.length > 0) {
            let hitCrate = intersects[0].object.parent;
            
            if(hitCrate.userData.box.scale.z > 3) {
              const uiCast = raycaster.intersectObjects(hitCrate.userData.UI.children);
              if (uiCast.length > 0) {
                if(hoveredButton) hoveredButton.material.emissive.set(uiColor)
                hoveredButton = uiCast[0].object;
                hoveredButton.material.emissive.set(0x000000);
              }
              else {
                hitCrate.userData.UI.children.forEach(btn => {
                  if(btn.material.emissive) btn.material.emissive.set(uiColor)
                });
                hoveredButton = null;
              }
            }
            if(hitCrate.userData.box.scale.z > 1.05)  return;

            // expand hitCrate; shrink all others
            this.shrinkAll(hitCrate);
          }
          else this.shrinkAll(); // if no hit, shrink any expanded crates
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
                  scale: {z: 1 + .4 +(crateObj.userData.textSize.max.z - crateObj.userData.textSize.min.z) + .4 * 6 },   // title + button panel width
                  position: {z:(.4 + (crateObj.userData.textSize.max.z - crateObj.userData.textSize.min.z) + .4 * 6 ) / 2}
                },
                UI: {
                  position: {z:1 + (crateObj.userData.textSize.max.z - crateObj.userData.textSize.min.z) + .4 * 6 }
                }
             }}, 1400) 
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
          let text = this.TextToPlane(serviceName, .5, 1, 80, uiColor);
          text.rotateY(Math.PI * 1.5);
          text.position.x -= 0.02;
          
          let textSize = new THREE.Box3().setFromObject(text);
          text.position.x -= .5;
          text.position.y -= .02;
          text.position.z -= ((textSize.max.z - textSize.min.z) / 2 + (btnSize * 6)) 
          textSize.setFromObject(text);
          uiGrp.add(text);

          // button placeholders
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
          btnStart.position.z = textSize.max.z + btnSize;
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
          btnStop.position.z = textSize.max.z + btnSize * 2;
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
          btnRestart.position.z = textSize.max.z + btnSize * 3;
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
          btnInfo.position.z = textSize.max.z + btnSize * 4;
          btnInfo.layers.enable(1);
          btnInfo.name = 'info'
          uiGrp.add(btnInfo);

          grp.add(uiGrp);

          // service image
          let serviceImgMat = new THREE.MeshPhongMaterial({
              side: THREE.FrontSide,
              map: imgLoader.load('./images/icons/' + this.services.find(s => s.name == serviceName).icon),
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
          // TODO: stagger
          grp.scale.set(0,0,0)
          let tScale = new TWEEN.Tween(grp.scale)
            .to({x: 1, y: 1, z: 1}, 750)
            .easing(TWEEN.Easing.Elastic.Out)
          tScale.start();

          this.crates.push(grp);
          scene.add(grp);
        },
        // credit to dcromley: https://discourse.threejs.org/t/an-example-of-text-to-canvas-to-texture-to-material-to-mesh-not-too-difficult/13757
        TextToPlane(txt, hWorldTxt, hWorldAll, hPxTxt, color) {
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
          let material = new THREE.MeshBasicMaterial( { side:THREE.FrontSide, map:new THREE.CanvasTexture(txtcanvas), 
            transparent:true, clippingPlanes: [clippingPlane], clipIntersection: true
          });
          
          return new THREE.Mesh(new THREE.PlaneGeometry(wWorldAll, hWorldAll), material);
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
        // triggered on bound services array change
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
        // UI click event
        onMouseDown(event) {
          if(!hoveredButton)  return;
          this.$emit('UI_event', hoveredButton.name + ' ' + hoveredButton.parent.parent.name)
        },
        // keep track of mouse position (normalized to [-1, 1])
        onMouseMove(event) {
          mousePos.x = ( event.clientX / window.innerWidth ) * 2 - 1;
          mousePos.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
        },
    },
}
</script>
