<template>
  <link rel="stylesheet" type="text/css" href="css/style.css">
    <HeaderContainer v-if="configLoaded"
      :APIOnline="isAPIOnline" 
      :config="this.config" 
      :title="config.title"
      @loadConfig="loadConfig" 
      @saveConfig="saveConfig" 
      ref="header"/>
    <ServiceContainer v-if="configLoaded"
      :fullscreen="!isAPIOnline" 
      :compactServices="config.compact_services" 
      :statusIndicators="config.enable_service_status" 
      :services="config.services" 
      :statuses="this.serviceStatuses"/>
    <DockerContainer v-if="configLoaded && isAPIOnline" 
      :backend="config.docker_api_backend" 
      @openSettings="this.$refs.header.showOptions = true"/>
    <CardContainer v-if="configLoaded && isAPIOnline" 
      :cards="config.cards" />
  <notifications position="top left" />
</template>

<script>
import HeaderContainer from './components/HeaderContainer.vue'
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
      config: {
        services: Array,
        cards: Array,
        minimal_mode: Boolean,
        docker_api_backend: String,
        title: String,
        compact_services: Boolean,
        enable_service_status: Boolean,
      },
      configLoaded: false,
      isOnline: true,
      pingTimer: Number,
      serviceStatuses: [],
    };
  },
  components: {
    HeaderContainer,
    ServiceContainer,
    DockerContainer,
    CardContainer
  },
  computed: {
    isAPIOnline() {
      if(this.config.minimal_mode == true)  return false;
      return this.isOnline;
    }
  },
  methods: {
    // request config from backend; fallback to local
    loadConfig: function() {
      this.axios.get('http://0.0.0.0:9101/readFrontendConfig').then((res) => {
        this.config = res.data;
      }).catch(() => {
        console.info('Failed to fetch config from backend. Loading local config.yml.')
        try {
          this.config = JsYaml.load(configFile);
          console.info('Successfully loaded local config.yml.') 
        } catch (e) {
          notifications.notifyError('Error: Failed to load configuration file');
        }
      }).finally(() => {
        // send service list to backend if status indicators enabled
        // TODO: rework service checker
        if(this.config.enable_service_status && !this.config.minimal_mode)  
          this.checkServices();
        this.configLoaded = true;
      });

    },
    // write settings to config.yml
    saveConfig() {
      this.axios.post('http://0.0.0.0:9101/writeFrontendConfig', this.config).then(() => {
        notifications.notifySuccess('Successfully saved configuration file');
      }).catch(() => { notifications.notifyError('Error: Failed to save configuration file'); });
    },
    // verify backend is up
    checkConnection() {
      if(this.config.minimal_mode == true) {
        clearInterval(this.pingTimer);
        return;
      }
      this.axios.get('http://0.0.0.0:9101/ping').then(() => { this.isOnline = true; })
        .catch(() => { this.isOnline = false; });

      if(this.config.minimal_mode == true && this.pingTimer) clearInterval(this.pingTimer);
    },
    // retrieve service statuses
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

    this.pingTimer = setInterval(this.checkConnection, 5000);
  },
  mounted() {
    this.checkConnection();

    // track up/down status of frontend application
    window.addEventListener('online', (() => { this.isOnline = true }));
    window.addEventListener('offline', (() => { this.isOnline = false; notifications.trackHidden = true; }));
  },
}
</script>
