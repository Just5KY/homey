<template>
  <Renderer ref="renderer" :pointer="{ intersectMode: 'frame' }" alpha antialias resize orbit-ctrl>
    <Camera :position="{ z: 10 }" />
    <Scene>
      <PointLight :position="{ y: 50, z: 50 }" />
      <Group ref="boxGroup">
        <Box @pointerEnter="mouseoverBox" @pointerLeave="mouseleaveBox" v-for="b in this.boxes" :key="b.name" :ref="'box' + boxes.indexOf(b)" 
          :position="{ x: boxes.indexOf(b) }"
          :size=".8">
          <LambertMaterial />
          <Text
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
          </Text>
        </Box>
      </Group>
      <GltfModel
        src="./models/scene.gltf"
        :position="{x:0, y: -.7, z: 0}"
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
    const boxGroup = this.$refs.boxGroup;
    const cursorPos = this.$refs.renderer.three.pointer.positionV3;
    renderer.three.setSize(this.width, this.height);

    renderer.onBeforeRender(() => {
      // iterate through boxes
      for(let i = 0; i < this.boxes.length; i++){
        let b = boxGroup.o3d.children[i]
        
      }
    });
  },
  methods: {
    mouseoverBox(event) {
      event.component.mesh.scale.z = 2;
      console.log(event.component.geometry)
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