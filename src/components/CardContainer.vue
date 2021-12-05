<template>
  <div class="card-container">
    <WeatherCard title="Weather"/>
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
