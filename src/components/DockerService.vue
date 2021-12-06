<template>
  <div class="docker-card-container">
    <h3>{{ serviceName }}</h3>
    <span>{{status}} - {{uptime}}</span>
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
