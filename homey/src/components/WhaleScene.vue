<template>
  <div id="three-canvas" ref="threeCanvas"></div>
</template>

<script>
//import { Clock, PerspectiveCamera, Scene, WebGLRenderer } from 'three'
import * as THREE from 'three';
import * as TWEEN from '@tweenjs/tween.js'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

// define three objects outside of vue export
// to avoid making them reactive
const scene = new THREE.Scene();
const clock = new THREE.Clock();
const raycaster = new THREE.Raycaster();
const gltfLoader = new GLTFLoader();
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


export default {
    name: 'WhaleScene',
    props: {
      services: Array,
    },
    data: function() {
        return {
            serviceData: [],
            crates: [],
            speed: 0.01,
            updateInterval: 2,  // seconds
            sinceLastUpate: 0.0,
            selectedCrate: null,
        };
    },
    // scene setup
    created: function() {
        this.serviceData = this.services;
				renderer.setPixelRatio( window.devicePixelRatio );
        
        scene.add(camera)
        scene.add(light)
        gltfLoader.load('./models/docker.glb', (model) => { 
          model.scene.position.y -= .75; 
          scene.add(model.scene); 
        });
        this.serviceData.forEach(s => {
          this.addCrate(s.name);
        });

        light.position.set(1, 5, 5);
        camera.position.z = 5;
        window.addEventListener('mousemove', this.onMouseMove, false );

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
    methods: {
        // main loop
        animate: function() {
            // refresh services every updateInterval seconds...
            this.sinceLastUpate += clock.getDelta();
            if(this.sinceLastUpate >= this.updateInterval) {
              // ...only if the service list has changed
              if(this.needsUpdate){
                this.updateCrates();
              }
              this.sinceLastUpate = 0.0;
            }

            this.raycast();
            TWEEN.update();
            controls.update();

            renderer.setSize(window.innerWidth, window.innerHeight);
            requestAnimationFrame(this.animate)
            renderer.render(scene, camera)
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
          const material = new THREE.MeshStandardMaterial({
              side: THREE.FrontSide,
              color: 'hsl(0, 100%, 50%)',
              wireframe: false
          })
          const geometry = new this.roundedBoxGeometry(1, 1, 1, .1, 8);

          let cube = new THREE.Mesh(geometry, material);
          let i = this.crates.length;
          cube.position.x += (i * 1.1);
          cube.scale.x = 0;
          cube.scale.y = 0;
          cube.scale.z = 0;
          cube.name = 'crate' + i.toString();
          this.crates.push({'meshName': cube.name, 'serviceName': serviceName})
          scene.add(cube);

          // TODO: stagger all spawn animations slightly at start
          const tween = new TWEEN.Tween(cube.scale)
            .to({x: 1, y: 1, z: 1}, 750)
            .easing(TWEEN.Easing.Elastic.Out)
          tween.start()
        },
        removeCrate(meshName) {
          let crateIndex = this.crates.findIndex(c => c.meshName == meshName);
          const tween = new TWEEN.Tween(scene.getObjectByName(meshName).scale)
            .to({x: 0, y: 0, z: 0}, 750)
            .easing(TWEEN.Easing.Elastic.In)
            .onComplete(() => { 
              this.crates.splice(crateIndex, 1); 
              scene.remove(scene.getObjectByName(meshName));
            });
          tween.start()
        },
        updateCrates() {
          // add crates for newly added services
          this.serviceData.forEach(s => {
            let found = false;
            this.crates.forEach(c => { if(s.name == c.serviceName) found = true; })
            if(!found) this.addCrate(s.name);
          });
          // remove crates for deleted services
          this.crates.forEach(c => {
            let found = false;
            this.serviceData.forEach(s => { if(s.name == c.serviceName) found = true; })
            if (!found) this.removeCrate(c.meshName);
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
    computed: {
        // check if any services have changed
        needsUpdate() {
          return this.crates.length != this.serviceData.length;
        },
    },
}
</script>
