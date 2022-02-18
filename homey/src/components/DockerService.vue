<template>
  <div :class="['docker-cell', 'd' + gridIndex, this.overflowClass, this.expansionClass]" 
    ref="cell" tabindex="0" @touchstart="expand" @mouseenter="expand" @mouseleave="contract" @touchend="contract">
    <img :src="'./data/icons/' + this.serviceName + '.png'" alt=""
      onerror="this.onerror=null; this.src='data/icons/default.png'">
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
  data () {
    return {
      overflowClass: '',
      expansionClass: '',
      infoString: this.state.charAt(0).toUpperCase() + this.state.slice(1) + ' - ' + this.uptime,
      pauseString: 'Pause ' + this.serviceName,
      stopString: 'Stop ' + this.serviceName,
      rebootString: 'Reboot ' + this.serviceName,
    };
  },
  mounted() {
    window.addEventListener('resize', this.calcOverflow)
    this.calcOverflow()
  },
  methods: {
    expand() {
      if (this.expansionClass == '')  this.expansionClass = 'docker-cell--expanded';
      //else this.expansionClass = ''
    },
    contract() {
      this.expansionClass = '';
    },
    passEmit(type){
      this.$emit('controlEvent', this.serviceName, type);
    },
    // if expansion would overflow page, shift to the left 
    calcOverflow() {
      let xPos = this.$refs.cell.getBoundingClientRect().x + 20;
      if( this.$refs.cell.scrollWidth > window.innerWidth - xPos ){
        this.overflowClass = 'docker-cell__overflow'
      }
      else {
        this.overflowClass = ''
      }
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
