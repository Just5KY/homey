<template>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat:100,200,300,400,500,600,700,800,900">
  <link rel="stylesheet" type="text/css" href="css/style.css">
  <Header @loadConfig="loadConfig" @saveConfig="saveConfig" :config="this.config" :title="config.title" ref="header"/>
  <ServiceContainer :fullscreen="config.minimal_mode" :statusIndicators="config.enable_service_status" :services="config.services" :statuses="this.serviceStatuses"/>
  <DockerContainer v-if="!config.minimal_mode" :backend="config.docker_api_backend" @openSettings="this.$refs.header.showOptions = true"/>
  <CardContainer v-if="!config.minimal_mode" />

  <notifications position="top left" />
</template>

<script>
import Header from './components/Header.vue'
import ServiceContainer from './components/ServiceContainer.vue'
import DockerContainer from './components/DockerContainer.vue'
import CardContainer from './components/CardContainer.vue'

import notifications from './notifications';

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
      } catch (e) { 
        notifications.notifyError('Error: Could not load configuration file');
      }
      finally{ 
        if(this.config.enable_service_status && !this.config.minimal_mode)  this.checkServices();  // send service list to backend for up/down checker
      }  
    },
    saveConfig() {
      this.axios.post('http://0.0.0.0:9101/writeFrontendConfig', this.config).then((res) => {
        notifications.notifySuccess('Successfully saved configuration file');
      }).catch(e => {
        notifications.notifyError('Error: Failed to save configuration file');
      });
    },
    checkServices: function() {
      this.axios.post('http://0.0.0.0:9101/updateServices', this.config.services).then((res) => {
          this.serviceStatuses = res.data;
      }).catch(e => {
        notifications.notifyWarning('Warning: Could not retrieve service uptime information');
      });
    }
  },
  beforeMount() {
    this.loadConfig();
  },
}
</script>
