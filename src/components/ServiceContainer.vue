<template>
  <div class="service-container">
    <h2>Services</h2>
    <ServiceCard title="Navidrome"/>
    <ServiceCard title="Jellyfin"/>
  </div>
</template>

<script>
import ServiceCard from './ServiceCard.vue'

export default {
  name: 'ServiceContainer',
  components: {
      ServiceCard
  }
}
</script>
