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
const controls = new OrbitControls(camera, renderer.domElement);
const gltfLoader = new GLTFLoader();
const fontLoader = new FontLoader();
const light = new THREE.DirectionalLight(0xffffff);
const invisMat = new THREE.MeshStandardMaterial({side: THREE.FrontSide, color: 0x000000, visible: false});

let mousePos = new THREE.Vector2(100, 100);
let defaultFont;
let boundingBoxes = [];

export default {
    name: 'WhaleScene',
    props: {
      services: Array,
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
        };
    },
    // scene setup
    created: function() {
        this.serviceData = this.services;

        // TODO: new font
        fontLoader.load('./fonts/helvetiker.json', (font) => {
          defaultFont = font;

          // spawn a crate for each service
          this.serviceData.forEach(s => {
            this.addCrate(s.name);
          })
        });

        // load whale
        gltfLoader.load('./models/docker.glb', (model) => { 
          model.scene.position.y -= .75; 
          scene.add(model.scene); 
        });

        scene.add(camera)
        scene.add(light)
        light.position.set(-5, 3, 2);
        camera.position.z = 5;
        
        renderer.setPixelRatio( window.devicePixelRatio );
        window.addEventListener('mousemove', this.onMouseMove, false );

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

            //this.updateBoundingBoxes();
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
          crateObj.userData.animation = new TWEEN.Tween(crateObj.userData.box)
            .to({
              scale: {z: 1 + .4 +(crateObj.userData.textSize.max.z - crateObj.userData.textSize.min.z) + .4 * 6 },   // title + button panel width
              position: {z:(.4 + (crateObj.userData.textSize.max.z - crateObj.userData.textSize.min.z) + .4 * 6 ) / 2}
             }, 1400) 
            .easing(TWEEN.Easing.Elastic.Out)
            .onUpdate(this.updateBoundingBoxes)
            .start();
        },
        // smooth shrink animation
        shrinkCrate(crateObj){
          if(crateObj.userData.box.scale.z < 1.05) return;

          if(crateObj.userData.animation) TWEEN.remove(crateObj.userData.animation);
          crateObj.userData.animation = new TWEEN.Tween(crateObj.userData.box)
            .to({ scale: {x: 1, z: 1, y: 1}, position: {z: 0} }, 600)
            .easing(TWEEN.Easing.Quadratic.Out)
            .onUpdate(this.updateBoundingBoxes)
            .start();
        },
        // new crate from service name
        addCrate(serviceName) {
          let grp = new THREE.Group();
          grp.name = serviceName;
          grp.position.x += (this.crates.length * 1.1);

          // rounded box
          const boxMat = new THREE.MeshStandardMaterial({
              side: THREE.FrontSide,
              color: 0xf8f8f8
          });
          let box = new THREE.Mesh(new RoundedBoxGeometry(1, 1, 1, 6, .1), boxMat);
          grp.add(box);

          // service name
          const textGeo = new TextGeometry(serviceName, {
            font: defaultFont,
            size: .3,
            height: .05,
            bevelEnabled: false,
          });
          const textMat = new THREE.MeshStandardMaterial({
              side: THREE.FrontSide,
              color: 0x00a7ff
          });
          let text = new THREE.Mesh(textGeo, textMat);
          text.rotateY(Math.PI * 1.5);
          
          let textSize = new THREE.Box3().setFromObject(text);
          text.position.x -= .5;
          text.position.y -= ((textSize.max.y - textSize.min.y) / 2);
          text.position.z += 1;
          textSize.setFromObject(text);
          grp.add(text);

          // button placeholders
          let btnSize = .4;
          const buttonGeo = new THREE.CircleGeometry(btnSize / 2, 32);
          const buttonMat = new THREE.MeshStandardMaterial({
              side: THREE.FrontSide,
              color: 0x00a7ff
          });
          const btnStart = new THREE.Mesh(buttonGeo, buttonMat);
          btnStart.rotateY(Math.PI * 1.5);
          btnStart.position.x = text.position.x - .05;
          btnStart.position.z = textSize.max.z + btnSize;
          grp.add(btnStart);

          const btnStop = new THREE.Mesh(buttonGeo, buttonMat);
          btnStop.rotateY(Math.PI * 1.5);
          btnStop.position.x = text.position.x - .05;
          btnStop.position.z = textSize.max.z + btnSize * 2;
          grp.add(btnStop);

          const btnRestart = new THREE.Mesh(buttonGeo, buttonMat);
          btnRestart.rotateY(Math.PI * 1.5);
          btnRestart.position.x = text.position.x - .05;
          btnRestart.position.z = textSize.max.z + btnSize * 3;
          grp.add(btnRestart);

          const btnInfo = new THREE.Mesh(buttonGeo, buttonMat);
          btnInfo.rotateY(Math.PI * 1.5);
          btnInfo.position.x = text.position.x - .05;
          btnInfo.position.z = textSize.max.z + btnSize * 4;
          grp.add(btnInfo);

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
            textSize: textSize
          };

          // elastic spawn animation
          // TODO: stagger all spawn animations slightly at start
          // grp.scale.set(0,0,0)
          // let tScale = new TWEEN.Tween(grp.scale)
          //   .to({x: 1, y: 1, z: 1}, 750)
          //   .easing(TWEEN.Easing.Elastic.Out)
          //   .onComplete(() => {
          //     grp.scale.set(1,1,1);
          //   });
          // tScale.start();

          this.crates.push(grp);
          scene.add(grp);
        },
        // remove existing crate
        removeCrate(crateObj) {
          boundingBoxes.splice(boundingBoxes.findIndex(b => b.name == crateObj.name + '_bbox'), 1);
          this.crates.splice(this.crates.indexOf(crateObj), 1);

          scene.remove(scene.getObjectByName(crateObj.name + '_bbox'));
          scene.remove(scene.getObjectByName(crateObj.name));
          
          // elastic despawn animation
          // const tScale = new TWEEN.Tween(crateObj.scale)
          //   .to({x: 0, y: 0, z: 0}, 750)
          //   .easing(TWEEN.Easing.Elastic.In)
          //   .onComplete(() => {   // remove when animation completes
          //   });
          // tScale.start()
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
        // keep track of mouse position (normalized to [-1, 1])
        onMouseMove(event) {
          mousePos.x = ( event.clientX / window.innerWidth ) * 2 - 1;
          mousePos.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
        },
    },
}
</script>
