<template>
  <div class="card-container">
    <WeatherCard title="Weather"/>
    <FloodCard title="Torrents"/>
  </div>
</template>

<script>
import WeatherCard from './WeatherCard.vue'
import FloodCard from './FloodCard.vue'

export default {
  name: 'CardContainer',
  components: {
      WeatherCard,
      FloodCard,
  },
  data() {
    return {
      apiCards: Array,
    };
  },
  methods: {
  }
}
</script>
