<template>
  <Renderer ref="renderer" :pointer="{ intersectMode: 'frame' }" alpha antialias resize orbit-ctrl>
    <Camera :position="{ z: 12 }" />
    <Scene>
      <PointLight :position="{ y: 50, z: 50 }" />
      <Group ref="boxGroup">
        <DockerService3D v-for="b in boxes" :key="b.name" :ref="'boxOuter' + boxes.indexOf(b)"
          :serviceName="b.name" :gridIndex="boxes.indexOf(b)" :size=".9" />
      </Group>
      <GltfModel src="./models/docker.glb" :position="{x:0, y: -.75, z: 0}" />
    </Scene>
  </Renderer>
</template>

<script>
import DockerService3D from './DockerService3D.vue';

export default {
  name: 'ThreeCanvas',
  props: {
    width: Number,
    height: Number,
    boxes: Array,
  },
  components: {
    DockerService3D,
  },
  mounted() {
    const renderer = this.$refs.renderer;
    const orbitCtrl = this.$refs.renderer.three.cameraCtrl;
    renderer.three.setSize(this.width, this.height);

    // camera settings
    orbitCtrl.maxAzimuthAngle = 0 + 0.2;  
    orbitCtrl.minAzimuthAngle = Math.PI / -2 - 0.2;
    orbitCtrl.maxPolarAngle = Math.PI / 2 + 0.2;
    orbitCtrl.minPolarAngle = Math.PI / 4;
    orbitCtrl.enablePan = false;
    orbitCtrl.enableDamping = true;
    orbitCtrl.dampingFactor = .03;
    // limit zoom
    // change to orth cam?

    renderer.onBeforeRender(() => {
      // iterate through boxes
      // for(let i = 0; i < this.boxes.length; i++){
      //   //let b = boxGroup.o3d.children[i]
        
      // }
    });
  },
  methods: {

  },
}
</script>

<style scoped>
  
</style>