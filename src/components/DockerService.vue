<template>
  <div class="docker-card-container">
    <h3>{{ serviceName }}</h3>
    <div class="docker-card-container__button-container">
      <span :title="pauseString" class="material-icons-outlined docker-card-btn">pause_circle</span>
      <span :title="rebootString" class="material-icons-outlined docker-card-btn">refresh</span>
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
      rebootString: 'Reboot ' + this.serviceName,
    };
  },
}
</script>
