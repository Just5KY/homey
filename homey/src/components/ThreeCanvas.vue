<template>
  <Renderer ref="renderer" :alpha="true" :antialias="true" :resize="true">
    <Camera :position="{ z: 10 }" />
    <Scene>
      <PointLight :position="{ y: 50, z: 50 }" />
      <Group ref="boxGroup">
        <Box v-for="b in this.boxes" :key="b.name" :ref="'box' + boxes.indexOf(b)" 
          :position="{ x: boxes.indexOf(b) }"
          :size=".8">
          <LambertMaterial />
        </Box>
      </Group>
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
    renderer.three.setSize(this.width, this.height);
    const boxGroup = this.$refs.boxGroup;

    renderer.onBeforeRender(() => {
      // spin
      for(let i = 0; i < this.boxes.length; i++){
        boxGroup.o3d.children[i].rotation.y += 0.01;
      }
      
    });
  },
}
</script>

<style scoped>
  
</style>