<template>
  <div :class="['docker-cell', 'd' + gridIndex]" ref="cell">
    <img v-if="!imageError" :src="getIconPath" @error="onImageError">
    <span v-if="imageError" class="docker-cell__image-placeholder material-icon icon-storage"></span>
    <div class="docker-cell__content">
      <h3>{{ serviceName }}</h3>
      <div class="docker-cell__content--buttons">
        <DockerServiceButton v-if="state=='running'" :serviceName="serviceName" type="pause"/>
        <DockerServiceButton v-if="state=='paused'" :serviceName="serviceName" type="unpause"/>
        <DockerServiceButton v-if="state=='exited'" :serviceName="serviceName" type="start"/>
        <DockerServiceButton v-if="state=='running' || state=='paused'" :serviceName="serviceName" type="stop"/>
        <DockerServiceButton v-if="state=='running' || state=='paused'" :serviceName="serviceName" type="restart"/>
        <DockerServiceButton @showDetailsPopup="emitToParent" :serviceName="serviceName" :serviceData="infoString" type="info"/>
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
  emits: [ 'showDetailsPopup' ],
  props: {
      gridIndex: Number,
      serviceName: String,
      state: String,
      uptime: String,
  },
  computed: {
    getIconPath: function() {
      return ((this.imageError) ? './data/icons/default.png' : './data/icons/' + this.serviceName + '.png')
    },
  },
  data () {
    return {
      infoString: this.state.charAt(0).toUpperCase() + this.state.slice(1) + ' - ' + this.uptime,
      pauseString: 'Pause ' + this.serviceName,
      stopString: 'Stop ' + this.serviceName,
      rebootString: 'Reboot ' + this.serviceName,
      imageError: false,
    };
  },
  methods: {
    emitToParent(containerData){
      this.$emit('showDetailsPopup', containerData);
    },
    onImageError: function() {
      this.imageError = true;
    },
    getYPos(){
      return this.$refs.cell.getBoundingClientRect().y;
    },
    // 8 rows, offset for 1-indexed grid__n-row class
    getYIndex(){
      return 9 - window.getComputedStyle(this.$refs.cell).getPropertyValue('grid-row-start');
    }
  },
}
</script>
