<template>
  <div class="header-container">
    <canvas class="header-animation"></canvas>
    <h1>{{ title }}</h1>
    <span v-if="!this.config.minimal_mode" @click="showOptions = !showOptions" title="Settings" class="material-icons-outlined">settings</span>
    <transition name="modal">
      <OptionsPopup v-if="showOptions" @loadConfig="loadConfig" @saveConfig="saveConfig" :config="this.config" @close="showOptions = false" tabindex="0" @keydown.esc="showOptions = false"/>
    </transition>
  </div>
</template>

<script>

import OptionsPopup from './OptionsPopup.vue';

export default {
  name: 'Header',
  components: {
    OptionsPopup,
  },
  props: {
    title: String,
    config: Object,
  },
  data: function() {
    return {
      showOptions: false,
    };
  },
  methods: {
    loadConfig() {
      this.$emit('loadConfig');
    },
    saveConfig() {
      this.$emit('saveConfig');
    },
  }
}
</script>