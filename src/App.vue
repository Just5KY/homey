<template>
    <div class="header">
      <h1>This will be my badass lightweight home dashboard.</h1>
    </div>
    <BookmarkBar :bookmarkList="bookmarks"></BookmarkBar>
    <div class="service-container">
        <ServiceCard v-for="srv in services" :key=srv.name :name=srv.name :url=srv.url :icon=srv.icon></ServiceCard>
    </div>
    <div class="widget-container">
      <ZenQuotesCard name="Zen Quote of the Day" url="https://zenquotes.io/api/random" :refreshInterval="30"></ZenQuotesCard>
      <NicehashCard name="Miner Status" url="https://placeholder.url" :refreshInterval="5"></NicehashCard>
    </div>
</template>

<script>

import BookmarkBar from './components/BookmarkBar.vue' 
import ServiceCard from './components/ServiceCard.vue'
import ZenQuotesCard from './components/ZenQuotesCard.vue'
import NicehashCard from './components/NicehashCard.vue'
// Navidrome API: http://music.mntn.top/rest/ping.view?u=steve=&p=babafrenchie8&v=1.16.1&c=apitest

export default {
  name: 'App',
  components: {
    ServiceCard,
    BookmarkBar,
    ZenQuotesCard,
    NicehashCard,
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
        { name: "Hacker News", url: "https://news.ycombinator.com"},
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

.service-container {
  width: 50%;
  margin: 0 auto;
}

body {
  background-color: #3a4652;
}

.api-card{
    border: 2px solid black;
    width: 50%;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem auto 1rem auto;
}

.api-card > p {
    font-size: 2rem;
    color: bisque;
}
</style>
