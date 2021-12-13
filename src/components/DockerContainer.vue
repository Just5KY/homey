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
  data () {
    return {
      dockerServices: Array,
    };
  },
  methods: {
    loadContainerList: function() {
      //   this.axios.get('http://0.0.0.0:9101/portainerList').then((res) => {
      //     // Sort by service name
      //     this.dockerServices = res.data.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
      // }).catch(e => {
      //   console.log('Could not reach homey API');
      // });
      this.dockerServices = 
[
  {
    "id": "66d7e3237e070895410c1a75836c4eb9e80b60b925a43ef472c29f0a7a42b148",
    "name": "rtorrent",
    "status": "running",
    "uptime": "Up 4 days"
  },
  {
    "id": "4ac67846318ef40f4ada0c8e491713765da47491753f0c4bd09cd436c954f92d",
    "name": "mealie",
    "status": "running",
    "uptime": "Up 3 days (healthy)"
  },
  {
    "id": "5cdc1aaa9605b0c6148290569fbf269109221b8b63cea19677d05707e17779e8",
    "name": "navidrome",
    "status": "running",
    "uptime": "Up 3 days (healthy)"
  },
  {
    "id": "0a3bee7a2d85b51bc389fcbe21a0d6dae507749974d72e8c6329ad20297bd522",
    "name": "portainer",
    "status": "running",
    "uptime": "Up 4 days"
  },
  {
    "id": "ea6a218960b9d35f08a41f7878aaa3c13a2610deb4dcdf3b59f5378ea4438ca8",
    "name": "hoppscotch",
    "status": "running",
    "uptime": "Up 4 days"
  },
  {
    "id": "b8fe9c8dbee3d0403d7091299c8818a51189d13f77491dcaab200e48579e6c1b",
    "name": "flood",
    "status": "running",
    "uptime": "Up 4 days"
  },
  {
    "id": "6e8b0d115850298cfc32faad8837a46e9fe26a45791339e6f8a0a7e58f835a94",
    "name": "jellyfin",
    "status": "running",
    "uptime": "Up 4 days"
  },
  {
    "id": "de2d8d8d58153da932b991482b9efa23da811d17a62d283926e36792064c6f8b",
    "name": "jackett",
    "status": "running",
    "uptime": "Up 3 days"
  },
  {
    "id": "69553ad774fa4dd3fcca8735c71355686d5d8ad5ee03d744aa6df84467248037",
    "name": "vaultwarden",
    "status": "running",
    "uptime": "Up 4 days (healthy)"
  },
  {
    "id": "7adbc3708cc84bb4ad2458207f1ab3c782a82d04a859773c1bc5d93c22981fb5",
    "name": "nginx-proxy-manager",
    "status": "running",
    "uptime": "Up 4 days"
  },
  {
    "id": "fed2c9b8b42245a5dfe85f7ac36de3cbd17f7ae08ef7d972c4ab50f591312fe7",
    "name": "nginx-proxy-manager-db",
    "status": "running",
    "uptime": "Up 4 days"
  },
  {
    "id": "ccda0e5745d691530028ecc013060f50930db7585f58624e4732d48461dade78",
    "name": "portainer-agent",
    "status": "running",
    "uptime": "Up 4 days"
  }
]

    },
    authenticate: function() {
        this.axios.get('http://0.0.0.0:9101/portainerAuth').then((res) => {
          //console.log('INFO :: Portainer authentication returned ' + res.data);
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
