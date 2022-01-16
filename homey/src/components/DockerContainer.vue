<template>
  <div class="docker-container">
    <div :class="gridClass">
      <DockerService v-for="(s, index) in dockerServices" 
        :key="index" 
        :gridIndex = "index+1" 
        :serviceName="s.name" 
        :state="s.status" 
        :uptime="s.uptime"
        ref="cell"
      />
    </div>
    <DockerControlPanel
      @toggleView="togglePerspective()"
      @refreshContainers="loadContainerList(true)"
      @openSettings="this.$emit('openSettings')" :perspective="this.perspective" />
    <img class="docker-container__whale" :src="'./images/docker-large-blank.png'">
  </div>
</template>

<script>
import DockerService from './DockerService.vue'
import DockerControlPanel from './DockerControlPanel.vue';

export default {
  name: 'DockerContainer',
  components: {
      DockerService,
      DockerControlPanel,
  },
  emits: ['openSettings'],
  props: {
    backend: String,
  },
  data() {
    return {
      dockerServices: Array,
      gridClass: 'docker-container__grid',
      perspective: '2d',
    };
  },
  computed: {
  },
  methods: {
    loadContainerList: function(shouldNotify=false) {
        this.axios.get('http://0.0.0.0:9101/' + this.backend + 'List').then((res) => {
          this.dockerServices = res.data;
      }).then(() => { 
        this.setGridSize();
        if (shouldNotify) this.$notify({
          title: 'Successfully refreshed container list',
          type: 'success'
        });
      }).catch(e => {
        console.warn('Error retrieving Docker containers. Is the selected Docker backend up and reachable?');
        this.$notify({
          title: 'Warning: Could not retrieve Docker container information',
          type: 'warn'
        })
      });

    },
    authenticate: function() {
        this.axios.get('http://0.0.0.0:9101/' + this.backend + 'Auth').then((res) => {
          //console.log('INFO :: ' + this.backend + ' API authentication returned ' + res.data);
      }).catch(e => {
        console.log('Error: Could not authenticate with ' + this.backend);
        this.$notify({
          title: 'Warning: Failed to authenticate with ' + this.backend,
          type: 'warn'
        })
      });
    },
    togglePerspective() {
      if(this.perspective == '2d')  this.perspective = '3d';
      else                          this.perspective = '2d';
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
