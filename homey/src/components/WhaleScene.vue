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

// define three.js objects outside of vue export
// to avoid making them reactive
const scene = new THREE.Scene();
const raycaster = new THREE.Raycaster();
const gltfLoader = new GLTFLoader();
const fontLoader = new FontLoader();
let mousePos = new THREE.Vector2(100, 100);
const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
)
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
const light = new THREE.DirectionalLight('hsl(0, 100%, 100%)');
let controls;
let defaultFont;

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
            selectedCrate: null,
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
        light.position.set(1, 5, 5);
        camera.position.z = 5;
        
        renderer.setPixelRatio( window.devicePixelRatio );
        window.addEventListener('mousemove', this.onMouseMove, false );

        // limit camera movement
        controls = new OrbitControls(camera, renderer.domElement);
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
          
          // closest hit is returned first; discard others
          // to avoid expanding crates behind the hovered one
          const intersects = raycaster.intersectObjects(scene.children);
          if(intersects.length > 0 && intersects[0].object.material.name != 'whale') {
            if(this.selectedCrate && this.selectedCrate.name == intersects[0].object.name)  return;
            if(this.selectedCrate)  this.shrinkCrate(this.selectedCrate);
            this.growCrate(intersects[0].object);
          }
          else {
            if (this.selectedCrate) {
              this.shrinkCrate(this.selectedCrate);
              this.selectedCrate = null;
            }
          }
        },
        growCrate(crateObj){
          // elastic pop out animation
          const tween = new TWEEN.Tween(crateObj.scale)
            .to({z: 3}, 1200)
            .easing(TWEEN.Easing.Elastic.Out)
          const tween2 = new TWEEN.Tween(crateObj.position)
            .to({z: 1}, 1200)
            .easing(TWEEN.Easing.Elastic.Out)
          tween.start()
          tween2.start()

          this.selectedCrate = crateObj;
        },
        shrinkCrate(crateObj){
          // smooth shrink animation
          const tween = new TWEEN.Tween(crateObj.scale)
            .to({z: 1}, 750)
            .easing(TWEEN.Easing.Quadratic.Out)
          const tween2 = new TWEEN.Tween(crateObj.position)
            .to({z: 0}, 750)
            .easing(TWEEN.Easing.Quadratic.Out)
          tween.start()
          tween2.start()
        },
        addCrate(serviceName) {
          let grp = new THREE.Group();
          grp.name = serviceName;

          // rounded box
          const boxMat = new THREE.MeshStandardMaterial({
              side: THREE.FrontSide,
              color: 'hsl(0, 100%, 50%)'
          });
          let box = new THREE.Mesh(new this.roundedBoxGeometry(1, 1, 1, .1, 8), boxMat);
          grp.add(box);

          // cheaper calculations for raycaster
          const boundingBox = new THREE.BoxHelper(box, 0x0000000);
          //boundingBox.material.visible = false;
          grp.add(boundingBox);

          // service name
          const textGeo = new TextGeometry(serviceName, {
            font: defaultFont,
            size: .1,
            height: .05,
            bevelEnabled: false,
          });
          const textMat = new THREE.MeshStandardMaterial({
              side: THREE.FrontSide,
              color: 0x00a7ff
          });
          let text = new THREE.Mesh(textGeo, textMat);
          text.rotateY(Math.PI * 1.5);
          text.position.x -= .5;
          let textSize = new THREE.Box3().setFromObject(text);
          text.position.z -= ((textSize.max.z - textSize.min.z) / 2);
          grp.add(text);

          grp.position.x += (this.crates.length * 1.1);
          grp.scale.set(0, 0, 0);

          this.crates.push(grp);
          scene.add(grp);

          // elastic spawn animation
          // TODO: stagger all spawn animations slightly at start
          const tween = new TWEEN.Tween(grp.scale)
            .to({x: 1, y: 1, z: 1}, 750)
            .easing(TWEEN.Easing.Elastic.Out);
          tween.start();
        },
        removeCrate(crateObj) {
          // elastic despawn animation
          const tween = new TWEEN.Tween(crateObj.scale)
            .to({x: 0, y: 0, z: 0}, 750)
            .easing(TWEEN.Easing.Elastic.In)
            .onComplete(() => {   // remove when animation completes
              this.crates.splice(this.crates.indexOf(crateObj), 1); 
              scene.remove(crateObj);
            });
          tween.start()
        },
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
        widthToScale(number) {
            // map a service name of length 0-255 to a scale factor which will appropriately resize box
            let fromRange = [0, 255];
            let toRange = [2, 45];
            return (((number - fromRange[0]) * (toRange[1] - toRange[0])) /
                (fromRange[1] - fromRange[0]) + toRange[0]);
        },

        // credit to prisoner849: https://discourse.threejs.org/t/round-edged-box/1402
        roundedBoxGeometry( width, height, depth, curveRadius, curveSegments ) {
          let shape = new THREE.Shape();
          let k = 0.00001;
          let radius = curveRadius - k;

          shape.absarc( k, k, k, -Math.PI / 2, -Math.PI, true );
          shape.absarc( k, height -  radius * 2, k, Math.PI, Math.PI / 2, true );
          shape.absarc( width - radius * 2, height -  radius * 2, k, Math.PI / 2, 0, true );
          shape.absarc( width - radius * 2, k, k, 0, -Math.PI / 2, true );

          return new THREE.ExtrudeBufferGeometry( shape, {
            depth: depth - curveRadius * 2,
            bevelEnabled: true,
            bevelSegments: curveSegments * 2,
            stk: 1,
            bevelSize: radius,
            bevelThickness: curveRadius,
            curveSegments: curveSegments
          }).center();
        },
    },
}
</script>
