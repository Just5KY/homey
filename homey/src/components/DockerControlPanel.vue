<template>
    <div class="docker-control-panel">
        <span class="material-icon icon-3d" 
            @click="this.$emit('toggleView')" title="Toggle view">
        </span>
        <span class="material-icon icon-refresh" 
            @click="this.$emit('refreshContainers')" title="Refresh containers">
        </span>
        <span class="material-icon icon-settings" 
            @click="this.$emit('openSettings')" title="Settings">
        </span>
    </div>
</template>

<script>
export default {
    name: 'DockerControlPanel',
    emits: ['toggleView', 'refreshContainers', 'openSettings']
}
</script>