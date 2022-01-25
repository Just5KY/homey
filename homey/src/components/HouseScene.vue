<template>
  <div id="house-canvas" ref="threeCanvas"></div>
</template>

<script>
import * as THREE from 'three';   // TODO: selective import
import * as TWEEN from '@tweenjs/tween.js'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

// define three.js objects outside of vue export
// to avoid making them reactive
const scene = new THREE.Scene();
const light = new THREE.HemisphereLight(0xffffbb, 0x000000, 2)
const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    100
);

const renderer = new THREE.WebGLRenderer({ 
  antialias: true, 
  alpha: true,
  logarithmicDepthBuffer: true,
});
const controls = new OrbitControls(camera, renderer.domElement);

// Geometry
const wallGeo = new THREE.BoxGeometry(1.05, 1.05, 0.05)
const roofGeo = new THREE.ConeGeometry(1, .77, 4)
const chimneyGeo = new THREE.BoxGeometry(.15, .6, .2)

// Materials
const wallMat = new THREE.MeshStandardMaterial({ 
    color: new THREE.Color(0x00ab9f), flatShading: false, roughness: .3, metalness: 0.3, side: THREE.FrontSide,
    polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1
})
const chimneyMat = new THREE.MeshStandardMaterial({ 
    color: new THREE.Color(0xFF5555), flatShading: false, roughness: 1, metalness: 0, side: THREE.FrontSide, 
})
const wireMat = new THREE.LineBasicMaterial({color: 0xf8f8f2})

// Meshes
const leftWall = new THREE.Mesh(wallGeo,wallMat)
const rightWall = new THREE.Mesh(wallGeo,wallMat)
const backWall = new THREE.Mesh(wallGeo,wallMat)
const frontWall = new THREE.Mesh(wallGeo,wallMat)
const roof = new THREE.Mesh(roofGeo, wallMat)
const chimney = new THREE.Mesh(chimneyGeo, chimneyMat)

leftWall.position.x -= .5
rotateDegrees(leftWall, 90)
rightWall.position.x += .5
rotateDegrees(rightWall, -90)
backWall.position.z -= .5
frontWall.position.z += .5
roof.position.y += 3
chimney.position.y -= 5
chimney.position.x += .35

let houseGroup;

export default {
    name: 'HouseScene',
    data: function() {
        return {
        };
    },
    // scene setup
    created: function() {    
        // camera + light
        light.position.set(0, 5, 0);
        camera.position.set(1.7, 1, -1.7);
        scene.add(light);
        scene.add(camera);

        // house
        this.initMeshes();
        chimney.scale.set(0, 0, 0);
        camera.lookAt(houseGroup);    
        
        renderer.setPixelRatio( window.devicePixelRatio );

        this.initControls();
    },
    // add canvas & begin animation loop
    mounted: function() {
        this.$refs.threeCanvas.appendChild(renderer.domElement);
        chimney.scale.set(0, 0, 0);

        this.initTweens();
        this.animate();
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

            // spin house
            houseGroup.rotation.y -= .01;

            renderer.setSize(width, height);
            requestAnimationFrame(this.animate)
            
            renderer.render(scene, camera); 
        },
        // update camera to canvas size
        updateCameraAspect(width, height){
          camera.aspect = width / height;
          camera.updateProjectionMatrix();
        },
        // camera settings
        initControls(){
          // limit movement
          controls.maxDistance = 8;
          controls.enablePan = false;
          // sense of inertia
          controls.enableDamping = true;
          controls.dampingFactor = .02;
        },
        // animations
        initTweens() {
          const startHeight = 7

          // roof
          const tween = new TWEEN.Tween({x: 0, y: startHeight, z: 0 })
              .to({x: 0, y: .9, z: 0 }, 3000)
              .easing(TWEEN.Easing.Bounce.Out)
              .onStart(() => {chimney.scale.set(0, 0, 0)})
              .onUpdate(function ({ x, y, z }, elapsed) {
                  roof.position.set(x, y, z)
          })
          const roofSpinTween = new TWEEN.Tween({rot: -100})
              .to({rot: 45}, 3000)
              .easing(TWEEN.Easing.Quadratic.InOut)
              .onUpdate(function ({rot}, elapsed) {
                  roof.rotation.y = THREE.MathUtils.degToRad(rot)
          })
          // chimney
          const chimneyTween = new TWEEN.Tween({x:.35, y: 0, z: 0})
              .to({x: .35, y: 1, z: 0}, 1200)
              .easing(TWEEN.Easing.Elastic.Out)
              .onStart(() => {chimney.scale.set(1, 1, 1)})
              .onUpdate(function ({x, y, z}, elapsed) {
                  chimney.position.set(x, y, z)
          })
          // left wall
          const leftTween = new TWEEN.Tween({x: leftWall.position.x, y: leftWall.position.y - startHeight, z: leftWall.position.z})
              .to({x: leftWall.position.x, y: leftWall.position.y, z: leftWall.position.z}, 2000)
              .easing(TWEEN.Easing.Bounce.Out)
              .onUpdate(function ({ x, y, z }, elapsed) {
                  leftWall.position.set(x, y, z)
          })
          // right wall
          const rightTween = new TWEEN.Tween({x: rightWall.position.x, y: rightWall.position.y - startHeight + .7, z: rightWall.position.z})
              .to({x: rightWall.position.x, y: rightWall.position.y, z: rightWall.position.z}, 2600)
              .easing(TWEEN.Easing.Bounce.Out)
              .onUpdate(function ({ x, y, z }, elapsed) {
                  rightWall.position.set(x, y, z)
          })
          // front wall
          const frontTween = new TWEEN.Tween({x: backWall.position.x, y: backWall.position.y - startHeight - .4, z: backWall.position.z})
              .to({x: backWall.position.x, y: backWall.position.y, z: backWall.position.z}, 1800)
              .easing(TWEEN.Easing.Bounce.Out)
              .onUpdate(function ({ x, y, z }, elapsed) {
                  backWall.position.set(x, y, z)
          })
          // back wall
          const backTween = new TWEEN.Tween({x: frontWall.position.x, y: frontWall.position.y - startHeight, z: frontWall.position.z})
              .to({x: frontWall.position.x, y: frontWall.position.y, z: frontWall.position.z}, 2900)
              .easing(TWEEN.Easing.Bounce.Out)
              .onUpdate(function ({ x, y, z }, elapsed) {
                  frontWall.position.set(x, y, z)
          })

          tween.chain(chimneyTween)
          tween.start()
          leftTween.start()
          rightTween.start()
          frontTween.start()
          backTween.start()
          roofSpinTween.start()
        },
        // house components
        initMeshes() {
          if(houseGroup)    return;

          houseGroup = new THREE.Group()
          houseGroup.add(leftWall)
          houseGroup.add(rightWall)
          houseGroup.add(backWall)
          houseGroup.add(frontWall)
          houseGroup.add(roof)
          houseGroup.add(chimney)

          scene.add(houseGroup);
        },
    },
}

// rotate mesh on Y axis
function rotateDegrees(mesh, degrees){
    const rad = degrees * Math.PI / 180;
    mesh.rotateY(rad)
}
</script>
