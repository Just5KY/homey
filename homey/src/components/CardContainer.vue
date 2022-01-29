<template>
  <div class="card-container">
    <FloodCard v-if="cardEnabled('Torrents')" />
    <WeatherCard v-if="cardEnabled('Weather')" />
    <BookmarkCard v-if="cardEnabled('Bookmarks')" />
    <SystemCard v-if="cardEnabled('System')" />
  </div>
</template>

<script>
import WeatherCard from './WeatherCard.vue'
import FloodCard from './FloodCard.vue'
import BookmarkCard from './BookmarkCard.vue'
import SystemCard from './SystemCard.vue'

export default {
  name: 'CardContainer',
  components: {
      WeatherCard,
      FloodCard,
      BookmarkCard,
      SystemCard
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
