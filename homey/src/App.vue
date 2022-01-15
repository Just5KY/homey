<template>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat:100,200,300,400,500,600,700,800,900">
  <link rel="stylesheet" type="text/css" href="css/style.css">
  <Header @loadConfig="loadConfig" @saveConfig="saveConfig" :config="this.config" :title="config.title"/>
  <ServiceContainer :fullscreen="config.minimal_mode" :statusIndicators="config.enable_service_status" :services="config.services" :statuses="this.serviceStatuses"/>
  <DockerContainer v-if="!config.minimal_mode" :backend="config.docker_api_backend"/>
  <CardContainer v-if="!config.minimal_mode" />

  <notifications position="top left" />
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
      config: Object,
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
        this.$notify({
          title: 'Successfully loaded configuration file',
          type: 'success'
        })
      } catch (e) { console.error('Error loading config file:' + e); }
      finally{ 
        if(this.config.enable_service_status && !this.config.minimal_mode)  this.checkServices();  // send service list to backend for up/down checker
      }  
    },
    saveConfig() {
      this.axios.post('http://0.0.0.0:9101/writeFrontendConfig', this.config).then((res) => {
        this.$notify({
          title: 'Successfully saved configuration file',
          type: 'success'
        })
      }).catch(e => {
        console.warn('Error writing configuration file. Are permissions correct?');
        this.$notify({
          title: 'Error: Failed to save configuration file',
          type: 'error'
        })
      });
    },
    checkServices: function() {
      this.axios.post('http://0.0.0.0:9101/updateServices', this.config.services).then((res) => {
          this.serviceStatuses = res.data;
      }).catch(e => {
        console.warn('Error checking services: could not reach homey API');
        this.$notify({
          title: 'Error: Could not retrieve service uptime information',
          type: 'error'
        })
      });
    }
  },
  beforeMount() {
    this.loadConfig();
  },
}
</script>
