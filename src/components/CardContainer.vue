<template>
  <div class="card-container">
    <h2>Information</h2>
    <APICard title="Weather"/>
    <APICard title="Server Control"/>
  </div>
</template>

<script>
import APICard from './APICard.vue'

export default {
  name: 'CardContainer',
  components: {
      APICard
  }
}
</script>
