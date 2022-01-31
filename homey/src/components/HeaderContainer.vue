<template>
  <div class="header-container">
    <div class="header-container__main">
      <HouseScene v-if="showHouse" />
      <div v-else class="header-container__main--house-padding"></div>
      <h1>{{ title }}</h1>
      <span v-if="APIOnline" 
        title="Settings" class="material-icon icon-settings"
        @click="showOptions = !showOptions">
      </span>
      <transition name="fade">
        <OptionsPopup v-if="showOptions" 
          :config="this.config"
          tabindex="0"
          @loadConfig="loadConfig" 
          @saveConfig="saveConfig" 
          @close="showOptions = false" 
          @keydown.esc="showOptions = false" />
      </transition>
    </div>
    <div class="header__offline-bar"
      v-if="!APIOnline && !config.minimal_mode">
      You're offline, bub
      <span class="material-icon icon-refresh" 
        @click="window.location.reload()" 
        title="Force refresh">
      </span>
    </div>
  </div>
</template>

<script>
import OptionsPopup from './OptionsPopup.vue';
import HouseScene from './HouseScene.vue';

export default {
  name: 'HeaderContainer',
  components: {
    OptionsPopup,
    HouseScene
  },
  props: {
    title: String,
    config: Object,
    APIOnline: Boolean,
  },
  data: function() {
    return {
      showOptions: false,
    };
  },
  computed: {
    showHouse() {
      if(this.config.hide_house)  return false;
      return !this.config.minimal_mode;
    },
  },
  methods: {
    loadConfig() {
      this.$emit('loadConfig');
    },
    saveConfig() {
      this.$emit('saveConfig');
    },
  },
}
</script>