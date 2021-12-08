<template>
  <div class="docker-card-container">
    <h3>{{ serviceName }}</h3>
    <div :title="uptime">{{status}} &nbsp;
      <span class="material-icons-outlined">pause_circle</span>
      <span class="material-icons-outlined">refresh</span>
      <span class="material-icons-outlined">info</span>
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
      
    };
  },
}
</script>
