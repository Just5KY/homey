<template>
  <div class="docker-card-container">
    <h3>{{ serviceName }}</h3>
    <div class="docker-card-container__button-container">
      <span  v-on:click="pauseContainer" :title="pauseString" class="material-icons-outlined docker-card-btn">pause_circle</span>
      <span  v-on:click="stopContainer" :title="stopString" class="material-icons-outlined docker-card-btn">stop_circle</span>
      <span  v-on:click="restartContainer" :title="rebootString" class="material-icons-outlined docker-card-btn">refresh</span>
      <span :title="infoString" class="material-icons-outlined docker-card-btn">info</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DockerService',
  props: {
      serviceName: String,
      status: String,
      uptime: String,
  },
  data () {
    return {
      infoString: this.status.charAt(0).toUpperCase() + this.status.slice(1) + ' (' + this.uptime + ')',
      pauseString: 'Pause ' + this.serviceName,
      stopString: 'Stop ' + this.serviceName,
      rebootString: 'Reboot ' + this.serviceName,
    };
  },
  methods: {
    pauseContainer: function(){
      this.axios.get('http://0.0.0.0:9101/portainerControl/' + this.serviceName + '/pause').then((res) => {
          if(res.data != 'success'){
            console.log("Error : " + res.data); }
      }).catch(e => { console.log('Could not reach homey API'); });
    },
    unpauseContainer: function(){
      this.axios.get('http://0.0.0.0:9101/portainerControl/' + this.serviceName + '/unpause').then((res) => {
          if(res.data != 'success'){
            console.log("Error : " + res.data); }
      }).catch(e => { console.log('Could not reach homey API'); });
    },
    stopContainer: function(){
      this.axios.get('http://0.0.0.0:9101/portainerControl/' + this.serviceName + '/stop').then((res) => {
          if(res.data != 'success'){
            console.log("Error : " + res.data); }
      }).catch(e => { console.log('Could not reach homey API'); });
    },
    startContainer: function(){
      this.axios.get('http://0.0.0.0:9101/portainerControl/' + this.serviceName + '/start').then((res) => {
          if(res.data != 'success'){
            console.log("Error : " + res.data); }
      }).catch(e => { console.log('Could not reach homey API'); });
    },
    restartContainer: function(){
      this.axios.get('http://0.0.0.0:9101/portainerControl/' + this.serviceName + '/restart').then((res) => {
          if(res.data != 'success'){
            console.log("Error : " + res.data); }
      }).catch(e => { console.log('Could not reach homey API'); });
    },
  }
}
</script>
