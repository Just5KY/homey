<template>
  <div class="docker-container">
    <div v-if="perspective == '2d'" :class="gridClass">
      <DockerService v-for="(s, index) in dockerServices" 
        :key="index" 
        :gridIndex = "index+1" 
        :serviceName="s.name" 
        :state="s.status" 
        :uptime="s.uptime"
        @showDetailsPopup="showDetailedInfo"
        ref="cell"
      />
    </div>
    <WhaleScene @3dClick="controlContainer" v-else ref="whale" :services="dockerServices" />
    <DockerControlPanel
      @toggleView="togglePerspective()"
      @refreshContainers="loadContainerList(true)"
      @openSettings="this.$emit('openSettings')" />
    <img v-if="perspective == '2d' && gridClass != 'docker-container__grid'" class="docker-container__whale" :src="'./images/docker-large-blank.png'">
    <div v-if="showDetails">{{ containerDetails }}</div>
  </div>
</template>

<script>
import WhaleScene from './WhaleScene.vue';
import DockerService from './DockerService.vue'
import DockerControlPanel from './DockerControlPanel.vue';
import notifications from '../notifications';

export default {
  name: 'DockerContainer',
  components: {
      DockerService,
      DockerControlPanel,
      WhaleScene,
  },
  emits: ['openSettings'],
  props: {
    backend: String,
  },
  data() {
    return {
      dockerServices: [],
      gridClass: 'docker-container__grid',
      perspective: '2d',
      refreshHandle: null,
      showDetails: false,
      containerDetails: {}
    };
  },
  computed: {
  },
  methods: {
    showDetailedInfo(containerData) {
      this.containerDetails = containerData;
      this.showDetails = true;
    },
    loadContainerList: function(shouldNotify=false) {
        this.axios.get('/api/' + this.backend + 'List').then((res) => {
          this.dockerServices = res.data;
      }).then(() => { 
        this.setGridSize();
        if (shouldNotify)   notifications.notifySuccess('Successfully refreshed container list');
      }).catch(e => {
        notifications.notifyWarning('Warning: Could not retrieve Docker container information');
      });
    },
    authenticate: function() {
        this.axios.get('/api/' + this.backend + 'Auth').then((res) => {
          //console.log('INFO :: ' + this.backend + ' API authentication returned ' + res.data);
      }).catch(e => {
        notifications.notifyWarning('Warning: Failed to authenticate with ' + this.backend);
      });
    },
    controlContainer: function(name, operation){
        let postData = {name: name, operation: operation};

        if(operation == 'info'){   
            let postData = {name: name, operation: 'info'}
            this.axios.post('/api/' + this.$parent.$parent.backend + 'Control',  postData).then((res) => {
              this.showDetailedInfo(res.data);
              return;
            })
        }

        notifications.notifyInfo('Attempting to ' + operation + ' container ' + name + '...');
        this.axios.post('/api/' + this.backend + 'Control', postData).then((res) => {
            if(res.data != 'success') throw 'controlException';
            notifications.notifySuccess('Successfully ' + operation + ((operation == 'pause' || operation == 'unpause') ? 'd' : 'ed') + ' container ' + name + '!');
            this.loadContainerList();
        }).catch(e => { 
            console.warn('Error: could not ' + operation + ' container ' + name + '. Is the selected ' + this.backend + ' backend up and reachable?'); 
        });
    },
    togglePerspective() {
      if(this.perspective == '2d')  this.perspective = '3d';

      else{
        this.$refs.whale.cleanup();
        this.perspective = '2d';

        // wait 25ms to ensure 2D services are present before grid size calc
        this.refreshHandle = setInterval(() => {
          this.setGridSize();
          clearInterval(this.refreshHandle);
        }, 25)
      }
    },
    // 3-row, 8-row, etc based on highest cell
    setGridSize(){
      if(!this.$refs.cell) return this.gridClass;
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
      //this.authenticate();  // auth is built into list function on backend
  },
}
</script>
