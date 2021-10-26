<template>
    <div class="header">
      <h1>Greetings planet! I'm learning Vue.js!<br>This will be my badass lightweight home dashboard.</h1>
    </div>
    <div class="card-container">
    <div v-for="srv in services" :key=srv.text>
      <ServiceCard :name=srv.name :url=srv.url :icon=srv.icon></ServiceCard>
    </div>
    </div>
  
</template>

<script>

import ServiceCard from './components/ServiceCard.vue'

export default {
  name: 'App',
  components: {
    ServiceCard,
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
    }
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
