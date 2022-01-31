<template>
  <div id="whale-canvas" ref="threeCanvas">
    <div ref="tooltip" id="tooltip">{{tooltipText}}</div>
  </div>
</template>

<script>
//import * as THREE from 'three';   // TODO: selective import
import { Vector2, Group, Mesh, BoxGeometry, MeshPhongMaterial, Box3, CanvasTexture, 
  SpriteMaterial, Sprite, MeshBasicMaterial, PlaneGeometry, TextureLoader, Scene, 
  /*OrthographicCamera,*/ PerspectiveCamera, WebGLRenderer, Raycaster, DirectionalLight, 
  AmbientLight, Plane, Vector3, FrontSide, BufferGeometryUtils, BufferGeometry } from 'three';
import { Tween, update as tweenUpdate, remove as tweenRemove, removeAll as tweenRemoveAll, Easing } from '@tweenjs/tween.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry';

import crateIndexes from '../crateIndexes';

let btnSize = .4;
let uiColor = 0x6272a4;
let mousePos = new Vector2(100, 100);
let boundingBoxes = [];
let hoveredButton;

// define three.js objects outside vue to avoid making them reactive
let scene, raycaster, light, ambientLight, camera, renderer, controls, clippingPlane;
let gltfLoader, imgLoader, invisMat, boxMat, buttonGeo, roundedBoxGeo;
let btnStartMat, btnRestartMat, btnPauseMat, btnUnpauseMat, btnStopMat, btnInfoMat, placeholderIconTex;

threeInitScene();
threeLoadAssets();
threeCreateAssets();

export default {
    name: 'WhaleScene',
    props: {
      services: Array,
    },
    emits: ['3dClick'],
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
        this.serviceData.forEach(s => { this.addCrate(s.name, s.status); });

        // for bounding boxes
        raycaster.layers.set(1);

        // lights & camera
        camera.position.set(-.25, 0, 8);
        scene.add(camera);

        light.position.set(-5, 5, 2);
        scene.add(ambientLight);
        scene.add(light);

        // initial camera transition animation
        const camSpawnTween = new Tween(camera).to({
          position: { 
            x: -8, 
            y: Math.max(this.services.length / 5, 2), 
            z: Math.max((this.services.length / 5) -.5, 3), 
          },
        }, 4000)
        .easing(Easing.Sinusoidal.InOut)
        .delay(1000)
        .onStart(() => { this.animationFinished = false; })
        //.onUpdate(() => { camera.updateProjectionMatrix() })  // ortho camera swap
        .onComplete(() => { this.animationFinished = true; })
        .start();
        
        renderer.setPixelRatio( window.devicePixelRatio );
        renderer.localClippingEnabled = true;

        this.initControls();
    },
    // add canvas, add listeners, begin animation loop
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

            tweenUpdate();
            controls.update();
            
            // do not raycast if initial camera transition is playing
            if(this.animationFinished)  this.raycast();     

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
          if(exceptCrate)   this.growCrate(exceptCrate);

          this.crates.forEach(c => {
            if(exceptCrate && c.name != exceptCrate.name)  this.shrinkCrate(c);
            else this.shrinkCrate(c);
          });
        },
        // elastic pop out animation
        growCrate(crateObj){
          if(crateObj.userData.box.scale.z > 1.05) return;

          if(crateObj.userData.animation) tweenRemove(crateObj.userData.animation);

          // title + button panel width
          let textWidth = crateObj.userData.textSize.max.z - crateObj.userData.textSize.min.z;
          crateObj.userData.animation = new Tween(crateObj)
            .to({ userData: {
                box: {
                  scale: {z: textWidth + .4 * 7 },   
                  position: {z:(-1 + textWidth + .4 * 7 ) / 2}
                },
                UI: {
                  position: {z: .25 + textWidth + .4 * 6 }
                }
             }}, 1600) 
            .easing(Easing.Elastic.Out)
            .onUpdate(this.updateBoundingBoxes)
            .onComplete((c) => { 
              c.userData.UI.children.forEach((btn, i) => {
                if(i != 0)  btn.layers.enable(1);
              }); 
            })
            .start();
        },
        // smooth shrink animation
        shrinkCrate(crateObj){
          if(crateObj.userData.box.scale.z < 1.05) return;

          if(crateObj.userData.animation) tweenRemove(crateObj.userData.animation);

          crateObj.userData.animation = new Tween(crateObj)
            .to({ userData: {
                box: {
                  scale: {x: 1, z: 1, y: 1}, 
                  position: {z: 0},
                },
                UI: {
                  position: {z: -2 + (crateObj.userData.textSize.max.z - crateObj.userData.textSize.min.z) / 2 - (.4 * 6) },
                }
             }}, 600)
            .easing(Easing.Quadratic.Out)
            .onUpdate(this.updateBoundingBoxes)
            .onStart((c) => { 
              c.userData.UI.children.forEach((btn) => {
                btn.layers.disable(1);
              }); 
            })
            .start();
        },
        // new crate from service name
        addCrate(serviceName, serviceStatus) {
          let grp = new Group();
          grp.name = serviceName;

          // position
          grp.position.x = crateIndexes.CrateIndexes[this.crates.length].x - 3.8;
          grp.position.y = crateIndexes.CrateIndexes[this.crates.length].y

          // rounded box          
          let box = new Mesh(roundedBoxGeo, boxMat);
          grp.add(box);

          // bounding box
          let bbox = new Mesh(new BoxGeometry(1, 1, 1), invisMat);
          bbox.name = grp.name + '_bbox';
          bbox.layers.enable(1);
          scene.add(bbox);
          bbox.parent = grp;
          boundingBoxes.push(bbox);

          // 2D elements
          let uiGrp = this.buildCrateUI(serviceName, serviceStatus);
          grp.add(uiGrp);

          // search for matching icon and load if exists
          imgLoader.load('./data/icons/' + serviceName + '.png', (tex) => {
            const serviceImgMat = new MeshPhongMaterial({ map: tex,
              side: FrontSide, transparent: true, });

            this.setCrateImage(serviceImgMat, grp, box);
          },
          undefined,
          // otherwise load default icon
          () => { this.setCrateImage(placeholderIconTex, grp, box); })

          // elastic spawn animation          
          grp.scale.set(0,0,0)
          let tScale = new Tween(grp.scale)
            .to({x: 1, y: 1, z: 1}, (Math.random() + 1) * 1500)   // slightly random stagger
            .easing(Easing.Elastic.Out)
            .delay(this.crates.length * 175)
          tScale.start();

          grp.userData = { 
            animation: null,
            box: box,
            UI: uiGrp,
            textSize: uiGrp.userData.textSize
          };

          this.crates.push(grp);
          scene.add(grp);
        },
        // draw icon on left & front of crate. box = rounded parent geometry
        setCrateImage(serviceImgMat, grp, box) {
          // front image
          const serviceImg = new Mesh(buttonGeo, serviceImgMat);
          serviceImg.position.z += .502;
          serviceImg.scale.set(1.5, 1.5, 1)
          grp.add(serviceImg);
          serviceImg.parent = box;

          // side image
          const serviceImgHidden = new Mesh(buttonGeo, serviceImgMat);
          serviceImgHidden.position.x -= .502;
          serviceImgHidden.scale.set(1.5, 1.5, 1)
          serviceImgHidden.rotateY(Math.PI * 1.5);      
          grp.add(serviceImgHidden);
        },
        // build 2D container control interface
        buildCrateUI(serviceName, serviceStatus){
          let uiGrp = new Group();
          
          // service name
          let text = this.TextToMesh(serviceName, .35, 1, 128, uiColor);
          text.rotateY(Math.PI * 1.5);
          text.position.x -= 0.02;
          
          let textSize = new Box3().setFromObject(text);
          text.position.x -= .5;
          text.position.z -= ((textSize.max.z - textSize.min.z) / 2 + (btnSize * 6)) 
          textSize.setFromObject(text);
          uiGrp.add(text);

          // buttons
          const btnPause = new Mesh(buttonGeo, btnPauseMat);
          btnPause.rotateY(Math.PI * 1.5);
          btnPause.position.x = text.position.x - .02;
          btnPause.position.z = textSize.max.z + (btnSize / 4);
          btnPause.name = 'pause'
          uiGrp.add(btnPause);

          const btnUnpause = new Mesh(buttonGeo, btnUnpauseMat);
          btnUnpause.rotateY(Math.PI * 1.5);
          btnUnpause.position.copy(btnPause.position);
          btnUnpause.name = 'unpause'
          uiGrp.add(btnUnpause);
 
          const btnStop = new Mesh(buttonGeo, btnStopMat);
          btnStop.rotateY(Math.PI * 1.5);
          btnStop.position.x = text.position.x - .02;
          btnStop.position.z = btnPause.position.z + btnSize;
          btnStop.name = 'stop'
          uiGrp.add(btnStop);

          const btnStart = new Mesh(buttonGeo, btnStartMat);
          btnStart.rotateY(Math.PI * 1.5);
          btnStart.position.copy(btnStop.position);
          btnStart.name = 'start'
          uiGrp.add(btnStart);
        
          const btnRestart = new Mesh(buttonGeo, btnRestartMat);
          btnRestart.rotateY(Math.PI * 1.5);
          btnRestart.position.x = text.position.x - .02;
          btnRestart.position.z = btnStop.position.z + btnSize;
          btnRestart.name = 'restart'
          uiGrp.add(btnRestart);
        
          const btnInfo = new Mesh(buttonGeo, btnInfoMat);
          btnInfo.rotateY(Math.PI * 1.5);
          btnInfo.position.x = text.position.x - .02;
          btnInfo.position.z = btnRestart.position.z + btnSize;
          btnInfo.name = 'info'
          uiGrp.add(btnInfo);

          switch (serviceStatus) {
            case 'paused':
              btnPause.scale.set(0, 0, 0); 
              btnUnpause.scale.set(1, 1, 1); 
              break;

            case 'stopped':
              btnStop.scale.set(0, 0, 0);
              btnStart.scale.set(1, 1, 1);
              btnPause.scale.set(0, 0, 0);
              btnUnpause.scale.set(0, 0, 0);
              break;
          
            default:
              btnStart.scale.set(0, 0, 0); 
              btnUnpause.scale.set(0, 0, 0); 
              break;
          }

          uiGrp.userData = { textSize: textSize };

          return uiGrp;
        },
        // remove existing crate
        removeCrate(crateObj) {
          boundingBoxes.splice(boundingBoxes.findIndex(b => b.name == crateObj.name + '_bbox'), 1);
          this.crates.splice(this.crates.indexOf(crateObj), 1);

          //elastic despawn animation
          const tScale = new Tween(crateObj.scale)
            .to({x: 0, y: 0, z: 0}, 750)
            .easing(Easing.Elastic.In)
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

          // update UI
          switch (hoveredButton.name) {
            case 'pause':
              hoveredButton.scale.set(0, 0, 0);
              hoveredButton.parent.getObjectByName('unpause').scale.set(1, 1, 1);
              hoveredButton = hoveredButton.parent.getObjectByName('unpause') 
              break;

            case 'unpause':
              hoveredButton.scale.set(0, 0, 0);
              hoveredButton.parent.getObjectByName('pause').scale.set(1, 1, 1);
              hoveredButton = hoveredButton.parent.getObjectByName('pause') 
              break;

            case 'stop':
              hoveredButton.scale.set(0, 0, 0);
              hoveredButton.parent.getObjectByName('pause').scale.set(0, 0, 0);
              hoveredButton.parent.getObjectByName('unpause').scale.set(0, 0, 0);
              hoveredButton.parent.getObjectByName('start').scale.set(1, 1, 1);
              hoveredButton = hoveredButton.parent.getObjectByName('start') 
              break;

            case 'start':
              hoveredButton.scale.set(0, 0, 0);
              hoveredButton.parent.getObjectByName('stop').scale.set(1, 1, 1);
              hoveredButton.parent.getObjectByName('pause').scale.set(1, 1, 1);
              hoveredButton = hoveredButton.parent.getObjectByName('stop') 
              break;
          
            default:
              break;
          }

          this.tooltipText = hoveredButton.name[0].toUpperCase() + hoveredButton.name.substring(1) + ' ' + hoveredButton.parent.parent.name;
        },
        // keep track of mouse position (normalized to [-1, 1])
        onMouseMove(event) {
          mousePos.x = ( (event.offsetX / this.$refs.threeCanvas.clientWidth)  ) * 2 - 1;
          mousePos.y = - ( (event.offsetY / this.$refs.threeCanvas.clientHeight) ) * 2 + 1;

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
          ctx.font = hPxTxt + "px Montserrat";   

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
          ctx.font = hPxTxt + "px Montserrat";    // needed after resize
          ctx.fillText(txt, wPxAll/2, hPxAll/2); 

          // create material + mesh from text
          let material;
          let textTexture = new CanvasTexture(txtcanvas)
          if(sprite){
            material = new SpriteMaterial({map: textTexture});
            return new Sprite(material)
          }
          else{
            material = new MeshBasicMaterial( { side:FrontSide, map: textTexture, 
              transparent:true, clippingPlanes: [clippingPlane], clipIntersection: true
            });
            return new Mesh(new PlaneGeometry(wWorldAll, hWorldAll), material);
          }
        },
        // destroy scene (triggered on 3D -> 2D swap)
        cleanup() {
          this.crates.forEach(c => {
            scene.remove(scene.getObjectByName(c.name + '_bbox'));
            scene.remove(scene.getObjectByName(c.name));
          });

          scene.remove(light);
          scene.remove(ambientLight);
          scene.remove(camera);

          boundingBoxes.splice(0, boundingBoxes.length);
          this.crates.splice(0, this.crates.length);
          tweenRemoveAll();
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
// load external assets that will not be reloaded on view swap
function threeLoadAssets() {
  gltfLoader = new GLTFLoader();
  imgLoader = new TextureLoader();

  // load UI images
  btnInfoMat = new MeshPhongMaterial({
      side: FrontSide, transparent: true, emissive: uiColor,
      clippingPlanes: [clippingPlane], clipIntersection: true,
      map: imgLoader.load('./images/ui/info.png')
  });
  btnRestartMat = new MeshPhongMaterial({
      side: FrontSide, transparent: true, emissive: uiColor,
      clippingPlanes: [clippingPlane], clipIntersection: true,
      map: imgLoader.load('./images/ui/restart.png')
  });
  btnPauseMat = new MeshPhongMaterial({
      side: FrontSide, transparent: true, emissive: uiColor,
      clippingPlanes: [clippingPlane], clipIntersection: true,
      map: imgLoader.load('./images/ui/pause.png')
  });
  btnStopMat = new MeshPhongMaterial({
      side: FrontSide, transparent: true, emissive: uiColor,
      clippingPlanes: [clippingPlane], clipIntersection: true,
      map: imgLoader.load('./images/ui/stop.png')
  });
  btnStartMat = new MeshPhongMaterial({
      side: FrontSide, transparent: true, emissive: uiColor,
      clippingPlanes: [clippingPlane], clipIntersection: true,
      map: imgLoader.load('./images/ui/start.png')
  });
  btnUnpauseMat = new MeshPhongMaterial({
      side: FrontSide, transparent: true, emissive: uiColor,
      clippingPlanes: [clippingPlane], clipIntersection: true,
      map: imgLoader.load('./images/ui/start.png')
  });
  // load fallback service icon
  placeholderIconTex = new MeshPhongMaterial({
      side: FrontSide, transparent: true,
      map: imgLoader.load('./data/icons/default.png')
  });
  
  // load whale
  gltfLoader.load('./models/whale_optimized.glb', (model) => { 
    model.scene.position.y -= .75;
    scene.add(model.scene); 
  });
}
// create geometries and materials that will not be destroyed on view swap
function threeCreateAssets() {
  invisMat = new MeshBasicMaterial({side: FrontSide, color: 0x000000, visible: false});
  boxMat = new MeshPhongMaterial({ side: FrontSide, color: 0xf8f8f2 });
   
  // imgLoader.load('./images/textures/crate_tex.png', (tex) => {
  //     crateTex = tex;
  //     boxMat = new MeshBasicMaterial({ map: crateTex, });
  //     crateTex.wrapS = RepeatWrapping;
  //     crateTex.needsUpdate = true;
  //   });

  buttonGeo = new PlaneGeometry(btnSize, btnSize);
  roundedBoxGeo = new RoundedBoxGeometry(1, 1, 1, 6, .1);
}
// create core three components outside of vue to avoid cascading DOM update every tick
function threeInitScene() {
  scene = new Scene();
  
  // orthographic camera
  // let width = window.innerWidth
  // let height = window.innerHeight
  // const camera = new OrthographicCamera( width / - 2, width / 2, height / 2, height / - 2, 1, 100 );

  camera = new PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 100);
  renderer = new WebGLRenderer({ antialias: true, alpha: true });
  controls = new OrbitControls(camera, renderer.domElement);
  raycaster = new Raycaster();

  // lights
  light = new DirectionalLight(0xffffff, 1.1);
  ambientLight = new AmbientLight(0xffffff, .2)
  light.position.set(-5, 5, 2);

  clippingPlane = new Plane(new Vector3(0, 0, 1), -.34);
}

</script>
