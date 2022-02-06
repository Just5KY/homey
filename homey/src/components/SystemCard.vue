<template>
  <div :class="getClass" @click="isFlipped = !isFlipped" @mouseleave="isFlipped = false">
      <div class="system-card-container__side system-card-container__side--front">
          <div class="system-card-container__heading">
            <span class="material-icon icon-memory system-card-container__heading__icon"></span>
            <span class="system-card-container__heading--title">System</span>
          </div>
          <div class="system-card-container__main">
            <SystemCardFrontChart v-if="isLoaded" :chartData="systemData" />
          </div>
      </div>
      <div class="system-card-container__side system-card-container__side--back">
          <div class="system-card-container__details--back">
            <h3>{{ systemData.hostname }}</h3>
            <p>Up {{ systemData.uptime }}</p>
          </div>
          <div class="system-card-container__disks">
            <SystemCardBackChart v-if="isLoaded" :chartData="systemData" />
          </div>
      </div>
  </div>
</template>

<script>
import SystemCardFrontChart from './SystemCardFrontChart.vue';
import SystemCardBackChart from './SystemCardBackChart.vue';
import notifications from '../notifications';

export default {
  name: 'SystemCard',
  components: {
      SystemCardFrontChart,
      SystemCardBackChart,
  },
  computed: {
    getClass() {
      return 'system-card-container' + ((this.isFlipped) ? ' system-card-container__flipped' : '' )
    },
  },
  data () {
    return {
      isFlipped: false,
      isLoaded: false,
      systemData: {}
    }
  },
  methods: {
    getSystemInfo: function() {
        this.axios.get('/api/systemInfo').then((res) => {
            this.systemData = res.data;
            this.isLoaded = true;
      }).catch(e => {
        console.warn('Error: Could not retrieve system information from homey API. Is monitorSystem.py running and outputting to the correct directory?');
        notifications.notifyWarning('Warning: Could not retrieve local system information');
      });
    },
  },
  created() {
    this.getSystemInfo()

    // Refresh system info every 30 seconds
    setInterval(() => {
      this.getSystemInfo()
    }, 30 * 1000)
  }
}
</script>
