<template>
  <div :class="getClass" @click="isFlipped = !isFlipped" @mouseleave="isFlipped = false">
      <div class="flood-card-container__side flood-card-container__side--front">
          <div class="flood-card-container__heading">
            <div class="flood-card-container__heading--stats">
              <div class="flood-card-container__heading--stats__up">
                <span class="material-icon icon-up_speed"></span><p>{{floodStats.upSpeed}}</p>
              </div>
              <div class="flood-card-container__heading--stats__down">
                <span class="material-icon icon-down_speed"></span><p>{{floodStats.downSpeed}}</p>
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
                <span class="material-icon icon-check"></span>
                <p>{{n.msg}}</p>
               </li>
            </ul>
          </div>
      </div>
  </div>
</template>

<script>
import { defineAsyncComponent } from 'vue';

export default {
  name: 'FloodCard',
  components: {
    FloodCardChart: defineAsyncComponent( () => 
      import('@/components/FloodCardChart.vue')
    )
  },
  data () {
    return {
      notifications: Array,
      floodStats: Object,
      loaded: false,
      isFlipped: false,
    }
  },
  computed: {
    getClass() {
      return 'flood-card-container' + ((this.isFlipped) ? ' flood-card-container__flipped' : '' )
    },
  },
  methods: {
    getFloodData: function() {
        this.axios.get('/api/floodNotifications').then((res) => {
          this.notifications = res.data;
      }).then(() => {
      this.axios.get('/api/floodStats').then((res) => {
        if(!res.data['Error']) {
          this.floodStats = res.data
          this.loaded = true;
        }
        else {
          this.notifications = [
            {
              msg: 'No response from Flood API',
              time: 'Now'
            }
          ]
        }
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
