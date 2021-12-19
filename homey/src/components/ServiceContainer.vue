<template>
  <div class="service-container">
      <ServiceCard v-for="s in services"
        :key="s.name"
        :title="s.name"
        :subtitle="s.subtitle"
        :icon="s.icon"
        :url="s.url" 
      />
  </div>
</template>

<script>
import ServiceCard from './ServiceCard.vue'

export default {
  name: 'ServiceContainer',
  props: {
    services: Array,
  },
  components: {
      ServiceCard
  }
}
</script>
