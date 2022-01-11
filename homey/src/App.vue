<template>
  <html>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat:100,200,300,400,500,600,700,800,900">
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <div class="button-container">
      <button @click="addService" id="add-box-btn">Add</button>
      <button @click="removeService" id="remove-box-btn">Del</button>
    </div>
    <WhaleScene :services="this.services" />
  </html>
</template>
<script>

import WhaleScene from './components/WhaleScene.vue';

export default {
  name: 'App',
  data() {
    return {
      services: [],
    };
  },
  components: {
    WhaleScene
  },
  methods: {
    addService() {
      this.services.push({"name": "Test Service " + this.services.length, "URL": "https://yandex.ru", "status": "Running"});
    },
    removeService() {
      this.services.pop();
    }
  },
  mounted() {
    this.addService();
  },
}
</script>

<style>
  .button-container {
    position: absolute;
    z-index: 10;
  }
  #three-canvas {
    position: absolute;
    height: 100%;
    width: 100%;
    top: 0;
    left: 0;
  }
</style>