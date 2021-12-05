<template>
  <div class="docker-card-container">
    <h3>{{ serviceName }}</h3>
    <div>{{status}} - {{uptime}}</div>
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
