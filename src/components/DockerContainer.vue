<template>
  <div class="docker-container">
    <DockerService v-for="s in dockerServices" :key="s.name" :serviceName="s.name" :status="s.status" :uptime="s.uptime"/>
  </div>
</template>

<script>
import DockerService from './DockerService.vue'

export default {
  name: 'DockerContainer',
  components: {
      DockerService
  },
  data () {
    return {
      dockerServices: Array,
    };
  },
  methods: {
    loadContainerList: function() {
        this.axios.get('http://0.0.0.0:9101/portainerList').then((res) => {
          this.dockerServices = res.data
      }).catch(e => {
        console.log('Could not reach homey API');
      });
    },
    // TODO: look into async. this should run before list, but doesn't need to as backend auto-auths on list call
    authenticate: function() {
        this.axios.get('http://0.0.0.0:9101/portainerAuth').then((res) => {
          console.log('INFO :: Portainer authentication returned ' + res.data);
      });
    },
  },
  beforeMount() {
      this.loadContainerList();
  },
}
</script>
