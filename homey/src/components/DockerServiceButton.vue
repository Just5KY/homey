<template>
    <span  v-on:click="controlContainer(this.type)" :title="getTooltip" class="material-icons-outlined docker-card-btn">{{getIcon}}</span>
</template>

<script>
export default {
    name: 'DockerServiceButton',
    props: {
      type: String,
      serviceName: String,
      serviceData: String,
    },
    computed: {
        getTooltip: function(){
            if(this.type == 'info'){
                return this.serviceData;
            }
            return this.type.charAt(0).toUpperCase() + this.type.slice(1) + ' ' + this.serviceName;
        },
        getIcon: function(){
            switch(this.type){
                case 'pause':
                    return 'pause_circle'
                case 'unpause':
                    return 'play_circle'
                case 'start':
                    return 'play_circle'
                case 'stop':
                    return 'stop_circle'
                case 'info':
                    return 'info'
                case 'restart':
                    return 'refresh'
            }
            return ''
        }
    },
    methods: {  
        controlContainer: function(operation){
            if(operation == 'info'){   
                return   // TODO: detailed info popup
            }
            this.axios.get('http://0.0.0.0:9101/' + this.$parent.$parent.backend + 'Control/' + this.serviceName + '/' + operation).then((res) => {
                if(res.data != 'success') throw 'controlException';

                this.$notify({
                    title: 'Successfully ' + operation + ((operation == 'pause' || operation == 'unpause') ? 'd' : 'ed') + ' container ' + this.serviceName + '!',
                    type: 'success'
                });
                this.$parent.$parent.loadContainerList();
            }).catch(e => { 
                console.warn('Error: could not ' + operation + ' container ' + this.serviceName + '. Is the selected Docker backend up and reachable?'); 
            });
        },
    },
}
</script>