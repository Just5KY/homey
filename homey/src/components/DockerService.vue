<template>
  <div :class="['docker-cell', 'd' + gridIndex]" ref="cell" tabindex="0">
    <img v-if="!imageError" :src="getIconPath" @error="onImageError">
    <span v-if="imageError" class="docker-cell__image-placeholder material-icon icon-storage"></span>
    <div class="docker-cell__content">
      <h3>{{ serviceName }}</h3>
      <div class="docker-cell__content--buttons">
        <DockerServiceButton type="pause" v-if="state=='running'"   
          @controlEvent="passEmit" :serviceName="serviceName" />
        <DockerServiceButton type="unpause" v-if="state=='paused'"  
          @controlEvent="passEmit" :serviceName="serviceName" />
        <DockerServiceButton type="start" v-if="state=='exited'"    
          @controlEvent="passEmit" :serviceName="serviceName" />
        <DockerServiceButton type="stop" v-if="state=='running' || state=='paused'"     
          @controlEvent="passEmit" :serviceName="serviceName" />
        <DockerServiceButton type="restart" v-if="state=='running' || state=='paused'"  
          @controlEvent="passEmit" :serviceName="serviceName" />
        <DockerServiceButton type="info" :serviceName="serviceName" 
          @controlEvent="passEmit" :serviceData="infoString" />
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
  emits: [ 'controlEvent' ],
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
    passEmit(type){
      this.$emit('controlEvent', this.serviceName, type);
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
