<template>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat:100,200,300,400,500,600,700,800,900">
  <link rel="stylesheet" type="text/css" href="css/style.css">
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Homey Dashboard"/>

  <div>
    MDI Icon Font:
    <span class="material-icons-outlined">home</span> <!-- Outlined -->
  </div>

  <canvas class="webgl"></canvas>

</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Montserrat, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 60px;
}
</style>
