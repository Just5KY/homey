<template>
  <div id="house-canvas" ref="threeCanvas"></div>
</template>

<script>
import { PerspectiveCamera, WebGLRenderer, Scene, Mesh, Group, 
    HemisphereLight, BoxGeometry, ConeGeometry, MeshBasicMaterial } from 'three';
import { randFloat, degToRad } from 'three/src/math/MathUtils';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { Tween, update, Easing } from '@tweenjs/tween.js'

// define three.js objects outside of vue export
// to avoid making them reactive
const scene = new Scene();
const light = new HemisphereLight(0xffffbb, 0x000000, 2)
const camera = new PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    100
);

const renderer = new WebGLRenderer({ 
  antialias: true, 
  alpha: true,
  logarithmicDepthBuffer: true,
});
const controls = new OrbitControls(camera, renderer.domElement);

// Geometry
const wallGeo = new BoxGeometry(1.05, 1.05, 0.05)
const roofGeo = new ConeGeometry(1, .77, 4)
const chimneyGeo = new BoxGeometry(.15, .6, .2)
// Materials
const wallMat = new MeshBasicMaterial({       color: 0xC2B280 });
const roofMat = new MeshBasicMaterial({       color: 0x282a36 });
const chimneyMat = new MeshBasicMaterial({    color: 0xE65F5C });
const windowMat = new MeshBasicMaterial({     color: 0x6272a4 });

// Meshes
const lwWall = new Mesh(wallGeo,wallMat)
const rwWall = new Mesh(wallGeo,wallMat)
const backWall = new Mesh(wallGeo,wallMat)
const frontWall = new Group()
const leftWall = new Group()
const rightWall = new Group()
const fwWall = new Mesh(wallGeo,wallMat)
const rwWindow = new Mesh(new BoxGeometry(.2, .35, .01), windowMat);
const lwWindow = new Mesh(new BoxGeometry(.2, .35, .01), windowMat);
const fwDoor = new Mesh(new BoxGeometry(.3, .45, .02),    windowMat);

frontWall.add(fwWall)
frontWall.add(fwDoor)
rightWall.add(rwWall)
rightWall.add(rwWindow)
leftWall.add(lwWall)
leftWall.add(lwWindow)

const roof = new Mesh(roofGeo, roofMat)
const chimney = new Mesh(chimneyGeo, chimneyMat)

leftWall.position.x -= .5
rotateDegrees(leftWall, 90)
rightWall.position.x += .5
rotateDegrees(rightWall, -90)
backWall.position.z -= .5

frontWall.position.z += .5
fwDoor.position.z += .03;
fwDoor.position.y -= .29;

lwWindow.position.x += (randFloat(-.3, .3))
rwWindow.position.x += (randFloat(-.3, .3))
rwWindow.position.z -= .03;
lwWindow.position.z -= .03;
rwWindow.position.y += (randFloat(-.1, .2))
lwWindow.position.y += (randFloat(-.1, .2))

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

            update();
            controls.update();

            // spin house
            houseGroup.rotation.y -= .007;

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
          const tween = new Tween({x: 0, y: startHeight, z: 0 })
              .to({x: 0, y: .9, z: 0 }, 3000)
              .easing(Easing.Bounce.Out)
              .onStart(() => {chimney.scale.set(0, 0, 0)})
              .onUpdate(function ({ x, y, z }, elapsed) {
                  roof.position.set(x, y, z)
          })
          const roofSpinTween = new Tween({rot: -100})
              .to({rot: 45}, 3000)
              .easing(Easing.Quadratic.InOut)
              .onUpdate(function ({rot}, elapsed) {
                  roof.rotation.y = degToRad(rot)
          })
          // chimney
          const chimneyTween = new Tween({x:.35, y: 0, z: 0})
              .to({x: .35, y: 1, z: 0}, 1200)
              .easing(Easing.Elastic.Out)
              .onStart(() => {chimney.scale.set(1, 1, 1)})
              .onUpdate(function ({x, y, z}, elapsed) {
                  chimney.position.set(x, y, z)
          })
          // left wall
          const leftTween = new Tween({x: leftWall.position.x, y: leftWall.position.y - startHeight, z: leftWall.position.z})
              .to({x: leftWall.position.x, y: leftWall.position.y, z: leftWall.position.z}, 2000)
              .easing(Easing.Bounce.Out)
              .onUpdate(function ({ x, y, z }, elapsed) {
                  leftWall.position.set(x, y, z)
          })
          // right wall
          const rightTween = new Tween({x: rightWall.position.x, y: rightWall.position.y - startHeight + .7, z: rightWall.position.z})
              .to({x: rightWall.position.x, y: rightWall.position.y, z: rightWall.position.z}, 2600)
              .easing(Easing.Bounce.Out)
              .onUpdate(function ({ x, y, z }, elapsed) {
                  rightWall.position.set(x, y, z)
          })
          // front wall
          const frontTween = new Tween({x: backWall.position.x, y: backWall.position.y - startHeight - .4, z: backWall.position.z})
              .to({x: backWall.position.x, y: backWall.position.y, z: backWall.position.z}, 1800)
              .easing(Easing.Bounce.Out)
              .onUpdate(function ({ x, y, z }, elapsed) {
                  backWall.position.set(x, y, z)
          })
          // back wall
          const backTween = new Tween({x: frontWall.position.x, y: frontWall.position.y - startHeight, z: frontWall.position.z})
              .to({x: frontWall.position.x, y: frontWall.position.y, z: frontWall.position.z}, 2900)
              .easing(Easing.Bounce.Out)
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

          houseGroup = new Group()
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
