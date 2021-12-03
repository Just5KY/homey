<template>
  <div class="service-card-container">
    <h3>{{ title }}</h3>
  </div>
</template>

<script>
export default {
  name: 'ServiceCard',
  props: {
      title: String,
  }
}
</script>
