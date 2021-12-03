<template>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat:100,200,300,400,500,600,700,800,900">
  <link rel="stylesheet" type="text/css" href="css/style.css">
  <Header title="Safehouse"/>
  <ServiceContainer/>
</template>

<script>
import Header from './components/Header.vue'
import ServiceContainer from './components/ServiceContainer.vue'
//import DockerContainer from './components/DockerContainer.vue'
//import CardContainer from './components/CardContainer.vue'

export default {
  name: 'App',
  components: {
    Header,
    ServiceContainer,
    // DockerContainer,
    // CardContainer
  }
}
</script>
