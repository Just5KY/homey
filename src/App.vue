<template>
    <div class="header">
      <h1>Greetings planet! I'm learning Vue.js!
        <br>This will be my badass lightweight home dashboard.
      </h1>
    </div>
    <div class="card-container">
        <ServiceCard v-for="srv in services" :key=srv.text :name=srv.name :url=srv.url :icon=srv.icon></ServiceCard>
    </div>
    <BookmarkBar id="bookmark-bar" :bookmarkList="bookmarks"></BookmarkBar>
</template>

<script>

import ServiceCard from './components/ServiceCard.vue'
//import APICard from './components/APICard.vue'
import BookmarkBar from './components/BookmarkBar.vue' 

export default {
  name: 'App',
  components: {
    ServiceCard,
    BookmarkBar,
  },
  data: function () {
    return {
      services: [
        { name: 'Whoogle', 
          url: 'https://mntn.top',
          icon: 'whoogle.png',
        },
        {
          name: 'Navidrome', 
          url: 'http://music.mntn.top',
          icon: 'navidrome.png',
        },
        {
          name: 'Nextcloud', 
          url: 'https://dokk.duckdns.org',
          icon: 'nextcloud.png',
        },
      ],
      bookmarks: [
        { name: "Redacted", url: "https://redacted.ch" },
        { name: "Hacker News", url: "https://news.ycombinator.com"}
      ],
    }
  },
  methods: {
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #a3a7ac;
  margin-top: 60px;
}

.card-container {
  width: 50%;
  margin: 0 auto;
}

body {
  background-color: #3a4652;
}
</style>
