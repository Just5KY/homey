<template>
  <div class="weather-card-container">
    <h2>Torrents</h2>
    <!-- <h3 style="text-align: center">{{floodStats.downSpeed}} Up | {{floodStats.upSpeed}} Down</h3> -->
    <div v-for="n in this.notifications" :key="n.time" class="weatherElement" >{{n.msg}} completed at {{n.time}}</div>
  </div>
</template>

<script>
export default {
  name: 'FloodCard',
  props: {
      title: String,
  },
  data () {
    return {
      notifications: Array,
      floodStats: Array,
    }
  },
  methods: {
    getFloodData: function() {
        this.axios.get('http://0.0.0.0:9101/floodNotifications').then((res) => {
          this.notifications = res.data.slice(0,5)
      }).catch(e => {
        console.log('Could not reach homey API');
      });
      this.axios.get('http://0.0.0.0:9101/floodStats').then((res) => {
          this.floodStats = res.data
      }).catch(e => {
        console.log('Could not reach homey API');
      });
    },
  },
  beforeMount() {
      this.getFloodData();
  },
}
</script>
