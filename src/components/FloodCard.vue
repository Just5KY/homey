<template>
  <div class="flood-card-container">
    <!-- <h3 style="text-align: center">{{floodStats.downSpeed}} Up | {{floodStats.upSpeed}} Down</h3> -->
    <!-- <div v-for="n in this.notifications" :key="n.time" class="weatherElement" >{{n.msg}} completed at {{n.time}}</div> -->
      <div class="flood-card-container__side flood-card-container__side--front">
          <div class="flood-card-container__heading">
            <div class="flood-card-container__heading--stats">
              <span class="material-icons-outlined">arrow_upward</span><p>{{floodStats.upSpeed}}</p>
              <span class="material-icons-outlined">arrow_downward</span><p>{{floodStats.downSpeed}}</p>
            </div>
            <span class="flood-card-container__heading--title">Torrents</span>
          </div>
          <div class="flood-card-container__details">
              <!-- chart goes here -->
          </div>
      </div>
      <div class="flood-card-container__side flood-card-container__side--back">
          <div class="flood-card-container__notifications">
            <ul>
              <li v-for="n in this.notifications" :key="n.time" class="weatherElement" >{{n.msg}}: Finished ({{n.time}})</li>
            </ul>
          </div>
      </div>
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
          this.notifications = res.data.slice(0,6)
      }).then(() => {
      this.axios.get('http://0.0.0.0:9101/floodStats').then((res) => {
          this.floodStats = res.data
      })}).catch(e => {
        console.log('Could not reach homey API');
      });
    },
  },
  mounted: function() {
    this.getFloodData();
    window.setInterval(() => {
      this.getFloodData()
    }, 5 * 1000)   // Refresh info every 5 seconds
  },
}
</script>
