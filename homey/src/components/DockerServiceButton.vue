<template>
    <span  v-on:click="controlContainer(this.type)" :title="getTooltip" :class="getIcon + ' material-icon docker-card-btn'"></span>
</template>

<script>
import notifications from '../notifications';

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
                    return 'icon-pause'
                case 'unpause':
                    return 'icon-play'
                case 'start':
                    return 'icon-play'
                case 'stop':
                    return 'icon-stop'
                case 'info':
                    return 'icon-info'
                case 'restart':
                    return 'icon-refresh'
            }
            return ''
        }
    },
    methods: {  
        controlContainer: function(operation){
            if(operation == 'info'){   
                return   // TODO: detailed info popup
            }
            notifications.notifyInfo('Attempting to ' + operation + ' container ' + this.serviceName + '...');
            let postData = {name: this.serviceName, operation: operation}
            this.axios.post('http://0.0.0.0:9101/' + this.$parent.$parent.backend + 'Control',  postData).then((res) => {
                if(res.data != 'success') throw 'controlException';
                notifications.notifySuccess('Successfully ' + operation + ((operation == 'pause' || operation == 'unpause') ? 'd' : 'ed') + ' container ' + this.serviceName + '!');
                this.$parent.$parent.loadContainerList();
            }).catch(e => { 
                console.warn('Error: could not ' + operation + ' container ' + this.serviceName + '. Is the selected Docker backend up and reachable?'); 
            });
        },
    },
}
</script>