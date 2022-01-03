<template>
  <html>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat:100,200,300,400,500,600,700,800,900">
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <button @click="addService" id="add-box-btn">Add</button>
    <ThreeCanvas :boxes="this.boxes" :height="500" :width="500" />
  </html>
</template>
<script>

import ThreeCanvas from './components/ThreeCanvas.vue'

export default {
  name: 'App',
  data() {
    return {
      boxes: [],
    };
  },
  components: {
    ThreeCanvas
  },
  methods: {
    addService() {
      this.boxes.push({"name": "Test Service!", "URL": "https://yandex.ru"});
    },
  },
  mounted() {
    this.addService();
  },
}
</script>

<style scoped>
  html {
    grid-column: 2;
  }
</style>