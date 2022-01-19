<template>
  <link rel="stylesheet" type="text/css" href="css/style.css">
  <Header @loadConfig="loadConfig" @saveConfig="saveConfig" :APIOnline="isAPIOnline" :config="this.config" :title="config.title" ref="header"/>
  <ServiceContainer :fullscreen="!isAPIOnline" :compactServices="config.compact_services" :statusIndicators="config.enable_service_status" :services="config.services" :statuses="this.serviceStatuses"/>
  <DockerContainer v-if="isAPIOnline" :backend="config.docker_api_backend" @openSettings="this.$refs.header.showOptions = true"/>
  <CardContainer v-if="isAPIOnline" />

  <notifications  position="top left" />
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
      isOnline: false,
      pingTimer: Number,
      serviceStatuses: [],
    };
  },
  components: {
    Header,
    ServiceContainer,
    DockerContainer,
    CardContainer
  },
  computed: {
    isAPIOnline() {
      return this.isOnline && !this.config.minimal_mode
    }
  },
  methods: {
    loadConfig: function() {
      try { 
        this.config = JsYaml.load(configFile);
      } catch (e) { 
        notifications.notifyError('Error: Could not load configuration file');
      }
      // send service list to backend for up/down checker
      finally{ 
        if(this.config.enable_service_status && !this.config.minimal_mode)  this.checkServices();
      }  
    },
    saveConfig() {
      this.axios.post('http://0.0.0.0:9101/writeFrontendConfig', this.config).then(() => {
        notifications.notifySuccess('Successfully saved configuration file');
      }).catch(() => {
        notifications.notifyError('Error: Failed to save configuration file');
      });
    },
    checkConnection() {
      this.axios.get('http://0.0.0.0:9101/ping').then(() => {
        this.isOnline = true;
      }).catch(() => { this.isOnline = false; });

      if(this.config.minimal_mode && this.pingTimer) clearInterval(this.pingTimer);
    },
    checkServices: function() {
      this.axios.post('http://0.0.0.0:9101/updateServices', this.config.services).then((res) => {
          this.serviceStatuses = res.data;
      }).catch(() => {
        if(this.isOnline) notifications.notifyWarning('Warning: Could not retrieve service uptime information');
      });
    }
  },
  beforeMount() {
    this.checkConnection();
    this.loadConfig();

    if(!this.config.minimal_mode) this.pingTimer = setInterval(this.checkConnection, 5000);
  },
  mounted() {
    this.checkConnection();

    window.addEventListener('online', (() => { this.isOnline = true }));
    window.addEventListener('offline', (() => { this.isOnline = false; notifications.trackHidden = true; }));
  },
}
</script>
