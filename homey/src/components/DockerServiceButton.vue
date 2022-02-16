<template>
    <span v-on:click="this.$emit('controlEvent', type)" 
        :title="getTooltip" 
        :class="getIcon + ' material-icon docker-card-btn'"></span>
</template>

<script>

export default {
    name: 'DockerServiceButton',
    props: {
      type: String,
      serviceName: String,
      serviceData: String,
    },
    emits: [ 'controlEvent' ],
    computed: {
        getTooltip: function(){
            if(this.type == 'info'){
                return (this.serviceData) ? this.serviceData : '';
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
        
    },
}
</script>