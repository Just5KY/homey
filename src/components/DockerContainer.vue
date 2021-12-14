<template>
  <div class="docker-container">
    <DockerService v-for="(s, index) in dockerServices" 
      :key="s.status" 
      :gridIndex = "index+1" 
      :serviceName="s.name" 
      :status="s.status" 
      :uptime="s.uptime"/>
  </div>
</template>

<script>
import DockerService from './DockerService.vue'

export default {
  name: 'DockerContainer',
  components: {
      DockerService
  },
  props: {
    backend: String,
  },
  data () {
    return {
      dockerServices: Array,
    };
  },
  methods: {
    loadContainerList: function() {
        this.axios.get('http://0.0.0.0:9101/' + this.backend + 'List').then((res) => {
          // Sort by service name
          //this.dockerServices = res.data.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
          this.dockerServices = res.data;
      }).catch(e => {
        console.log('Could not reach homey API');
      });

    },
    authenticate: function() {
        this.axios.get('http://0.0.0.0:9101/' + this.backend + 'Auth').then((res) => {
          //console.log('INFO :: ' + this.backend + ' API authentication returned ' + res.data);
      });
    },
  },
  mounted: function() {
    this.loadContainerList();
    window.setInterval(() => {
      this.loadContainerList()
    }, 30 * 1000)   // Refresh container info every 30 seconds
  },
  beforeMount() {
      this.authenticate();
  },
}
</script>
