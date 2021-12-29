<template>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat:100,200,300,400,500,600,700,800,900">
  <link rel="stylesheet" type="text/css" href="css/style.css">
  <Header title="homey"/>
  <ServiceContainer :displayStatus="config.enable_service_status" :services="config.services" :statuses="this.serviceStatuses"/>
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
      serviceStatuses: [],
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
      this.checkServices(); // send service list to backend for up/down checker
    },
    checkServices: function() {
      this.axios.post('http://0.0.0.0:9101/updateServices', this.config.services).then((res) => {
          this.serviceStatuses = res.data;
      }).catch(e => {
        console.log('Could not reach homey API');
      });
    }
  },
  beforeMount() {
    this.loadConfig();
  },
}
</script>
