<template>
  <div class="flood-card-container">
      <div class="flood-card-container__side flood-card-container__side--front">
          <div class="flood-card-container__heading">
            <div class="flood-card-container__heading--stats">
              <div class="flood-card-container__heading--stats__up">
                <span class="material-icons-outlined">arrow_upward</span><p>{{floodStats.upSpeed}}</p>
              </div>
              <div class="flood-card-container__heading--stats__down">
                <span class="material-icons-outlined">arrow_downward</span><p>{{floodStats.downSpeed}}</p>
              </div>
            </div>
            <span class="flood-card-container__heading--title">Torrents</span>
          </div>
          <div class="flood-card-container__chart">
              <FloodCardChart v-if="this.loaded" :chartData="floodStats.minuteData"/>
          </div>
      </div>
      <div class="flood-card-container__side flood-card-container__side--back">
          <div class="flood-card-container__notifications">
            <ul>
              <li v-for="n in this.notifications" :key="n.time" :title="'Finished ' + n.time" >
                <span class="material-icons-outlined">check</span>
                <p>{{n.msg}}</p>
               </li>
            </ul>
          </div>
      </div>
  </div>
</template>

<script>

import FloodCardChart from './FloodCardChart.vue';

export default {
  name: 'FloodCard',
  components: {
    FloodCardChart,
  },
  props: {
      title: String,
  },
  data () {
    return {
      notifications: Array,
      floodStats: Object,
      loaded: false,
    }
  },
  methods: {
    getFloodData: function() {
        this.axios.get('http://0.0.0.0:9101/floodNotifications').then((res) => {
          this.notifications = res.data;
      }).then(() => {
      this.axios.get('http://0.0.0.0:9101/floodStats').then((res) => {
          this.floodStats = res.data
          this.loaded = true;
      })}).catch(e => {
        console.info('Warning: Could not reach Flood API. The API could be overloaded - it is usually safe to ignore this message.');
      });
    },
  },
  mounted: function() {
    this.getFloodData();
    window.setInterval(() => {
      this.getFloodData()
    }, 10 * 1000)   // Refresh info every 10 seconds
  },
}
</script>
