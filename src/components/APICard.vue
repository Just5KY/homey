<template>
  <div class="api-card-container">
    <h3>{{ title }}</h3>
  </div>
</template>

<script>
export default {
  name: 'APICard',
  props: {
      title: String,
  }
}
</script>
