<template>
  <Renderer ref="renderer" :pointer="{ intersectMode: 'frame' }" alpha antialias resize orbit-ctrl>
    <Camera :position="{ z: 12 }" />
    <Scene>
      <PointLight :position="{ y: 50, z: 50 }" />
      <Group ref="boxGroup">
        <Box @pointerEnter="mouseoverBox" @pointerLeave="mouseleaveBox"
          v-for="b in this.boxes" :key="b.name" :ref="'box' + boxes.indexOf(b)" 
          :position="{ x: boxes.indexOf(b) - 2.6 }"
          :size=".9">
          <!-- convert to matcap / baked in material & nix light -->
          <LambertMaterial />
          <!-- <Text
            :text="b.name"
            font-src="./fonts/helvetiker.json"
            align="center"
            :size=".2"
            :height=".2"
            :position="{ x: 0, y: 0, z: 0 }"
            :rotation="{y: Math.PI / -2}"
            :cast-shadow="true"
          >
            <PhongMaterial />
          </Text> -->
        </Box>
      </Group>
      <GltfModel
        src="./models/no_boxes.gltf"
        :position="{x:0, y: -.75, z: 0}"
      />
    </Scene>
  </Renderer>
</template>

<script>
export default {
  name: 'ThreeCanvas',
  props: {
    width: Number,
    height: Number,
    boxes: Array,
  },
  mounted() {
    const renderer = this.$refs.renderer;
    const orbitCtrl = this.$refs.renderer.three.cameraCtrl;
    renderer.three.setSize(this.width, this.height);

    // camera settings
    orbitCtrl.maxAzimuthAngle = 0 + 0.2;  
    orbitCtrl.minAzimuthAngle = Math.PI / -2 + 0.1;
    orbitCtrl.maxPolarAngle = Math.PI / 2 + 0.2;
    orbitCtrl.minPolarAngle = Math.PI / 4;
    orbitCtrl.enablePan = false;
    orbitCtrl.enableDamping = true;
    orbitCtrl.dampingFactor = .03;

    renderer.onBeforeRender(() => {
      // iterate through boxes
      // for(let i = 0; i < this.boxes.length; i++){
      //   //let b = boxGroup.o3d.children[i]
        
      // }
    });
  },
  methods: {
    mouseoverBox(event) {
      event.component.mesh.scale.z = 2;
    },
    mouseleaveBox(event) {
      event.component.mesh.scale.z = 1;
    },
    whaleLoaded() {

    }
  },
}
</script>

<style scoped>
  
</style>