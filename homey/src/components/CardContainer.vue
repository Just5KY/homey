<template>
  <div class="card-container">
    <FloodCard v-if="cardEnabled('Torrents')" />
    <WeatherCard v-if="cardEnabled('Weather')" />
    <BookmarkCard v-if="cardEnabled('Bookmarks')"
      :bookmarks="bookmarks" />
    <SystemCard v-if="cardEnabled('System')" />
  </div>
</template>

<script>
import { defineAsyncComponent } from 'vue'

export default {
  name: 'CardContainer',
  components: {
      WeatherCard: defineAsyncComponent(() => import('@/components/WeatherCard.vue')),
      FloodCard: defineAsyncComponent(() => import('@/components/FloodCard.vue')),
      BookmarkCard: defineAsyncComponent(() => import('@/components/BookmarkCard.vue')),
      SystemCard: defineAsyncComponent(() => import('@/components/SystemCard.vue'))
  },
  props: {
    cards: Array,
    bookmarks: Array,
  },
  data() {
    return {
    };
  },
  methods: {
    cardEnabled(name) {
      return this.cards.find(c => c.name === name).enable;
    },
  },
}
</script>
