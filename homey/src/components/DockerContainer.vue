<template>
  <div class="docker-container">
    <div :class="gridClass">
      <DockerService v-for="(s, index) in dockerServices" 
        :key="index" 
        :gridIndex = "index+1" 
        :serviceName="s.name" 
        :status="s.status" 
        :uptime="s.uptime"
        ref="cell"
      />
    </div>
    <!-- <img class="docker-container__whale" :src="'./images/docker-large-blank.png'"> -->
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
  data() {
    return {
      dockerServices: Array,
      gridClass: 'docker-container__grid',
    };
  },
  computed: {
  },
  methods: {
    loadContainerList: function() {
        this.axios.get('http://0.0.0.0:9101/' + this.backend + 'List').then((res) => {
          // Sort by service name
          //this.dockerServices = res.data.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
          this.dockerServices = res.data;
      }).then(() => { this.setGridSize() }).catch(e => {
        console.log('Could not reach homey API');
      });

    },
    authenticate: function() {
        this.axios.get('http://0.0.0.0:9101/' + this.backend + 'Auth').then((res) => {
          //console.log('INFO :: ' + this.backend + ' API authentication returned ' + res.data);
      }).catch(e => {
        console.log('Could not reach homey API');
      });
    },
    // 3-row, 8-row, etc based on highest cell
    setGridSize(){
      if(!this.$refs.cell) return 'docker-container__grid';
      let highRow = 0;
      this.$refs.cell.forEach(c => {
        if(c.getYIndex() > highRow) highRow = c.getYIndex();
      });
      this.gridClass = 'docker-container__grid docker-container__grid__' + highRow.toString() + '-row';
    }
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
