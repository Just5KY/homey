<template>
  <div class="docker-card-container">
    <h3>{{ serviceName }}</h3>
    <div class="docker-card-container__button-container">
      <DockerServiceButton v-if="state=='running'" :serviceName="serviceName" type="pause"/>
      <DockerServiceButton v-if="state=='paused'" :serviceName="serviceName" type="unpause"/>
      <DockerServiceButton v-if="state=='exited'" :serviceName="serviceName" type="start"/>
      <DockerServiceButton v-if="state=='running' || state=='paused'" :serviceName="serviceName" type="stop"/>
      <DockerServiceButton v-if="state=='running' || state=='paused'" :serviceName="serviceName" type="restart"/>
      <DockerServiceButton :serviceName="serviceName" :serviceData="infoString" type="info"/>
    </div>
  </div>
</template>

<script>

import DockerServiceButton from './DockerServiceButton.vue';

export default {
  name: 'DockerService',
  components: {
    DockerServiceButton,
  },
  props: {
      serviceName: String,
      status: String,
      uptime: String,
  },
  data () {
    return {
      infoString: this.status.charAt(0).toUpperCase() + this.status.slice(1) + ' - ' + this.uptime,
      pauseString: 'Pause ' + this.serviceName,
      stopString: 'Stop ' + this.serviceName,
      rebootString: 'Reboot ' + this.serviceName,
      state: this.status,
    };
  },
  computed: {

  },
  methods: {

  },
}
</script>
