<template>
    <div class="docker-control-panel">
        <span class="material-icons-outlined" 
            @click="this.$emit('toggleView')" title="Toggle view mode">
        3d_rotation</span>
        <span class="material-icons-outlined" 
            @click="this.$emit('refreshContainers')" title="Refresh containers">
        refresh</span>
        <span class="material-icons-outlined" 
            @click="this.$emit('openSettings')" title="Settings">
        settings</span>
    </div>
</template>

<script>
export default {
    name: 'DockerControlPanel',
    emits: ['toggleView', 'refreshContainers', 'openSettings']
}
</script>