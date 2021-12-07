<template>
  <div class="card-container">
    <WeatherCard title="Weather"/>
    <WeatherCard title="Placeholder"/>
  </div>
</template>

<script>
import WeatherCard from './WeatherCard.vue'

export default {
  name: 'CardContainer',
  components: {
      WeatherCard
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
