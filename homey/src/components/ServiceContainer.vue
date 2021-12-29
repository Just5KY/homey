<template>
  <div :class="getClass">
      <ServiceCard v-for="s in services"
        :key="s.name"
        :title="s.name"
        :subtitle="s.subtitle"
        :icon="s.icon"
        :url="s.url"
        :displayStatus="this.statusIndicators"
        :isUp="this.getStatus(s.name)" 
      />
  </div>
</template>

<script>
import ServiceCard from './ServiceCard.vue'

export default {
  name: 'ServiceContainer',
  props: {
    services: Array,
    statuses: Array,
    statusIndicators: Boolean,
    fullscreen: Boolean,
  },
  computed: {
    getClass: function() {
      return ((this.fullscreen) ? 'service-container service-container__fullscreen' : 'service-container');
    },
  },
  components: {
      ServiceCard
  },
  methods: {
    getStatus: function(serviceName) {
      for(let i=0; i < this.statuses.length; i++){
        if(this.statuses[i].name == serviceName){
          return this.statuses[i].up;
        }
      }
    }
  },
}
</script>
