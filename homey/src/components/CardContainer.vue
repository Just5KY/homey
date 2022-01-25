<template>
  <div class="card-container">
    <FloodCard v-if="cardEnabled('Torrents')" />
    <WeatherCard v-if="cardEnabled('Weather')" />
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
  props: {
    cards: Array,
  },
  data() {
    return {
      apiCards: Array,
    };
  },
  methods: {
    cardEnabled(name) {
      return this.cards.find(c => c.name === name).enable;
    },
  },
}
</script>
