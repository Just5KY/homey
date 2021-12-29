<template>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat:100,200,300,400,500,600,700,800,900">
  <link rel="stylesheet" type="text/css" href="css/style.css">
  <Header title="homey"/>
  <ServiceContainer :services="config.services" />
  <DockerContainer :backend="config.docker_api_backend"/>
  <CardContainer/>
</template>

<script>
import Header from './components/Header.vue'
import ServiceContainer from './components/ServiceContainer.vue'
import DockerContainer from './components/DockerContainer.vue'
import CardContainer from './components/CardContainer.vue'

import JsYaml from 'js-yaml';

import configFile from './assets/config.yml'

export default {
  name: 'App',
  data() {
    return {
      config: this.config,
    };
  },
  components: {
    Header,
    ServiceContainer,
    DockerContainer,
    CardContainer
  },
  methods: {
    loadConfig: function() {
      try { 
        this.config = JsYaml.load(configFile);
      } catch (e) { console.log('Error loading config file:' + e); }
      // try {
      //   // axios POST send service list to API
      // } catch (e) {}
    },
  },
  beforeMount() {
    this.loadConfig();
  },
}
</script>
