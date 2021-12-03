<template>
  <div class="docker-container">
    <h2>Docker</h2>
    <DockerService title="portainer"/>
    <DockerService title="flood"/>
  </div>
</template>

<script>
import DockerService from './DockerService.vue'

export default {
  name: 'DockerContainer',
  components: {
      DockerService
  }
}
</script>
