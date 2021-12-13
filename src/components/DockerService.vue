<template>
  <!-- <div class="docker-card-container"> -->
  <div :class="['docker-cell', 'd' + gridIndex]">
    <img :src="'./images/icons/' + serviceName + '.png'">
    <div class="docker-cell__content">
      <h3>{{ serviceName }}</h3>
      <div class="docker-cell__content--buttons">
        <DockerServiceButton v-if="state=='running'" :serviceName="serviceName" type="pause"/>
        <DockerServiceButton v-if="state=='paused'" :serviceName="serviceName" type="unpause"/>
        <DockerServiceButton v-if="state=='exited'" :serviceName="serviceName" type="start"/>
        <DockerServiceButton v-if="state=='running' || state=='paused'" :serviceName="serviceName" type="stop"/>
        <DockerServiceButton v-if="state=='running' || state=='paused'" :serviceName="serviceName" type="restart"/>
        <DockerServiceButton :serviceName="serviceName" :serviceData="infoString" type="info"/>
      </div>
      
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
      gridIndex: Number,
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
