import { createApp } from 'vue'
import App from './App.vue'

import '@material-design-icons/font';

import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import * as TWEEN from '@tweenjs/tween.js'
import * as dat from 'dat.gui'

createApp(App).mount('#app')

// Debug
//const gui = new dat.GUI()

// Canvas
const canvas = document.querySelector('canvas.header-animation')

// Scene
const scene = new THREE.Scene()

// Geometry
const leftPlane = new THREE.BoxGeometry(1.05, 1.05, 0.05)
const rightPlane = new THREE.BoxGeometry(1.05, 1.05, 0.05)
const backPlane = new THREE.BoxGeometry(1.05, 1.05, 0.05)
const frontPlane = new THREE.BoxGeometry(1.05, 1.05, 0.05)
const roof = new THREE.ConeGeometry(1, .77, 4)
const chimney = new THREE.BoxGeometry(.15, .6, .2)

// Materials
const material = new THREE.MeshStandardMaterial({ 
    color: new THREE.Color(0x00ab9f), flatShading: false, roughness: .3, metalness: 0.3, side: THREE.FrontSide,
    polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1
})
const chimneyMaterial = new THREE.MeshStandardMaterial({ 
    color: new THREE.Color(0xFF5555), flatShading: false, roughness: 1, metalness: 0, side: THREE.FrontSide, 
})
const wireMaterial = new THREE.LineBasicMaterial({color: 0xf8f8f2})

// Meshes
const m1 = new THREE.Mesh(leftPlane,material)
const m2 = new THREE.Mesh(rightPlane,material)
const m3 = new THREE.Mesh(backPlane,material)
const m4 = new THREE.Mesh(frontPlane,material)
const roofMesh = new THREE.Mesh(roof, material)
const chimneyMesh = new THREE.Mesh(chimney, chimneyMaterial)

// left
m1.position.x -= .5
rotateDegrees(m1, 90)
// right
m2.position.x += .5
rotateDegrees(m2, -90)
// back
m3.position.z -= .5
// front
m4.position.z += .5
// roof
roofMesh.position.y += 3
// chimney
chimneyMesh.position.y += 40
chimneyMesh.position.x += .35

// Wireframes
const g4 = new THREE.WireframeGeometry(m4.geometry)
const frontWire = new THREE.LineSegments(g4, wireMaterial)
frontWire.position.z += .5

// animation
const startHeight = 7
// roof
const tween = new TWEEN.Tween({x: 0, y: startHeight, z: 0 })
    .to({x: 0, y: .9, z: 0 }, 3000)
    .easing(TWEEN.Easing.Bounce.Out)
    .onUpdate(function ({ x, y, z }, elapsed) {
        roofMesh.position.set(x, y, z)
})
const roofSpinTween = new TWEEN.Tween({rot: -100})
    .to({rot: 45}, 3000)
    .easing(TWEEN.Easing.Quadratic.InOut)
    .onUpdate(function ({rot}, elapsed) {
        roofMesh.rotation.y = THREE.MathUtils.degToRad(rot)
})
// chimney
const chimneyTween = new TWEEN.Tween({x:.35, y: 0, z: 0})
    .to({x: .35, y: 1, z: 0}, 1200)
    .easing(TWEEN.Easing.Elastic.Out)
    .onUpdate(function ({x, y, z}, elapsed) {
        chimneyMesh.position.set(x, y, z)
})
// left wall
const leftTween = new TWEEN.Tween({x: m1.position.x, y: m1.position.y - startHeight, z: m1.position.z})
    .to({x: m1.position.x, y: m1.position.y, z: m1.position.z}, 2000)
    .easing(TWEEN.Easing.Bounce.Out)
    .onUpdate(function ({ x, y, z }, elapsed) {
        m1.position.set(x, y, z)
})
// right wall
const rightTween = new TWEEN.Tween({x: m2.position.x, y: m2.position.y - startHeight + .7, z: m2.position.z})
    .to({x: m2.position.x, y: m2.position.y, z: m2.position.z}, 2600)
    .easing(TWEEN.Easing.Bounce.Out)
    .onUpdate(function ({ x, y, z }, elapsed) {
        m2.position.set(x, y, z)
})
// front wall
const frontTween = new TWEEN.Tween({x: m3.position.x, y: m3.position.y - startHeight - .4, z: m3.position.z})
    .to({x: m3.position.x, y: m3.position.y, z: m3.position.z}, 1800)
    .easing(TWEEN.Easing.Bounce.Out)
    .onUpdate(function ({ x, y, z }, elapsed) {
        m3.position.set(x, y, z)
})
// back wall
const backTween = new TWEEN.Tween({x: m4.position.x, y: m4.position.y - startHeight, z: m4.position.z})
    .to({x: m4.position.x, y: m4.position.y, z: m4.position.z}, 2900)
    .easing(TWEEN.Easing.Bounce.Out)
    .onUpdate(function ({ x, y, z }, elapsed) {
        m4.position.set(x, y, z)
})

tween.chain(chimneyTween)
tween.start()
leftTween.start()
rightTween.start()
frontTween.start()
backTween.start()
roofSpinTween.start()

// Grouping
const houseGroup = new THREE.Group()
houseGroup.add(m1)
houseGroup.add(m2)
houseGroup.add(m3)
houseGroup.add(m4)
houseGroup.add(roofMesh)
houseGroup.add(chimneyMesh)
//houseGroup.add(frontWire)
houseGroup.scale.x = .9
houseGroup.scale.y = .9
houseGroup.scale.z = .9
scene.add(houseGroup)

//Lights
// const pointLight = new THREE.PointLight(0xffffff, 5)
// pointLight.position.x = 2
// pointLight.position.y = 3
// pointLight.position.z = 4
// scene.add(pointLight)
// const light2 = new THREE.PointLight(0xffffff, 1)
// light2.position.x = -2
// light2.position.y = -3
// light2.position.z = -4
// scene.add(light2)
const sun = new THREE.HemisphereLight(0xffffbb, 0x000000, 2)
scene.add(sun)

// Functions
function rotateDegrees(mesh, degrees){
    const rad = degrees * Math.PI / 180
    mesh.rotateY(rad)
}

// Boilerplate
const sizes = {
    width: 120,
    height: 160
}

// Camera
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 100)
camera.position.x = 2
camera.position.y = 1
camera.position.z = -2
scene.add(camera)
camera.lookAt(houseGroup.position)

// Controls
const controls = new OrbitControls(camera, canvas)
controls.enableDamping = true

// Renderer
const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    alpha: true,
    antialias: true,
    logarithmicDepthBuffer: true,
})
renderer.setSize(sizes.width, sizes.height)
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
renderer.autoClear = false;

// Resize
window.addEventListener('resize', () =>
{
    // Update sizes
    sizes.width = window.innerWidth
    sizes.height = window.innerHeight

    // Update camera
    camera.aspect = sizes.width / sizes.height
    camera.updateProjectionMatrix()

    // Update renderer
    renderer.setSize(sizes.width, sizes.height)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
})

// Main loop
const clock = new THREE.Clock()
const tick = () =>
{
    const elapsedTime = clock.getElapsedTime()

    // Update objects
    TWEEN.update()
    houseGroup.rotation.y = -.5 * elapsedTime

    controls.update()

    // Render
    renderer.render(scene, camera)

    // Call tick again on the next frame
    window.requestAnimationFrame(tick)
}

// Entrypoint
tick()
