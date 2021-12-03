<template>
  <div class="docker-service-container">
    <h3>{{ title }}</h3>
  </div>
</template>

<script>
export default {
  name: 'DockerService',
  props: {
      title: String,
  }
}
</script>
