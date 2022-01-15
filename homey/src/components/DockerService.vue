<template>
  <!-- <div class="docker-card-container"> -->
  <div :class="['docker-cell', 'd' + gridIndex]" ref="cell">
    <img v-if="!imageError" :src="getIconPath" @error="onImageError">
    <span v-if="imageError" class="docker-cell__image-placeholder material-icons-outlined">storage</span>
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
  computed: {
    getIconPath: function() {
      return ((this.imageError) ? './images/icons/placeholder.png' : './images/icons/' + this.serviceName + '.png')
    },
  },
  data () {
    return {
      infoString: this.status.charAt(0).toUpperCase() + this.status.slice(1) + ' - ' + this.uptime,
      pauseString: 'Pause ' + this.serviceName,
      stopString: 'Stop ' + this.serviceName,
      rebootString: 'Reboot ' + this.serviceName,
      state: this.status,
      imageError: false,
    };
  },
  methods: {
    onImageError: function() {
      this.imageError = true;
    },
    getYPos(){
      return this.$refs.cell.getBoundingClientRect().y;
    },
    getYIndex(){
      return window.getComputedStyle(this.$refs.cell).getPropertyValue('grid-column');
    }
  },
}
</script>
