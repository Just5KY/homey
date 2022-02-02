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
      :cards="config.cards"
      :bookmarks="config.bookmarks" />
  <notifications position="top left" />
</template>

<script>
import HeaderContainer from './components/HeaderContainer.vue'
import ServiceContainer from './components/ServiceContainer.vue'
import DockerContainer from './components/DockerContainer.vue'
import CardContainer from './components/CardContainer.vue'

import notifications from './notifications';

import JsYaml from 'js-yaml';

export default {
  name: 'App',
  data() {
    return {
      config: {},
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
      if(!this.configLoaded || this.config.minimal_mode)  return false;
      return this.isOnline;
    }
  },
  methods: {
    // load configuration
    loadConfig: function() {
      // fetch from backend
      this.axios.get('/api/readFrontendConfig').then((res) => {
        this.config = res.data;
        this.configLoaded = true;
      }).catch(() => {
        // on error, fall back to local file
        console.info('Failed to fetch config from backend. Loading local config.yml.')
        this.axios.get('/config/config.yml').then((res) => {
          this.config = JsYaml.load(res.data);
          this.configLoaded = true;
        }).catch(() => {
          notifications.notifyError('Error: Failed to load configuration file');
        });
      })
      .finally(() => {
        this.checkConnection();
      } );
    },
    // write settings to config.yml
    saveConfig() {
      this.axios.post('/api/writeFrontendConfig', this.config).then(() => {
        notifications.notifySuccess('Successfully saved configuration file');
        window.location.reload();
      }).catch(() => { notifications.notifyError('Error: Failed to save configuration file'); });
    },
    // verify backend is up
    checkConnection() {
      if(this.config.minimal_mode == true) {
        clearInterval(this.pingTimer);
        return;
      }
      this.axios.get('/api/ping').then(() => { 
        this.isOnline = true;
        if(this.config.enable_service_status) this.checkServices(); 
      }).catch(() => { this.isOnline = false; });

      if(this.config.minimal_mode == true && this.pingTimer) clearInterval(this.pingTimer);
    },
    // retrieve service statuses
    checkServices: function() {
      this.axios.get('/api/checkServices').then((res) => { 
        this.serviceStatuses = res.data;
      }).catch(() => {
        if(this.isOnline) notifications.notifyWarning('Warning: Could not retrieve service uptime information');
      });
    }
  },
  created() {
    this.checkConnection();
    this.loadConfig();

    this.pingTimer = setInterval(this.checkConnection, 5000);
  },
  mounted() {
    // track up/down status of frontend application
    window.addEventListener('online', (() => { this.isOnline = true }));
    window.addEventListener('offline', (() => { this.isOnline = false; notifications.trackHidden = true; }));
  },
}
</script>
