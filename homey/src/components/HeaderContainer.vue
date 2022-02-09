<template>
  <div class="header-container">
    <div class="header-container__main">
      <HouseScene v-if="showHouse" />
      <div v-else class="header-container__main--house-padding"></div>
      <h1>{{ title }}</h1>
      <div v-if="config.bookmarks_in_header" class="header-container__main--bookmark-container">
          <a :href="b.url" v-for="b in config.bookmarks" :key="b.name" class="bookmark"
             :title="b.hover">
              <h3>{{b.name}}</h3>
              <span class="material-icon icon-arrow_right bookmark__arrow"></span>
          </a>
      </div>
      <span v-if="APIOnline" 
        title="Settings" :class="getSettingsIconClass"
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
    <transition name="fade">
      <div class="header__offline-bar"
        v-if="!APIOnline && !config.minimal_mode">
        Offline
        <span class="material-icon icon-offline" 
          @click="window.location.reload()" 
          title="Force refresh">
        </span>
      </div>
    </transition>
  </div>
</template>

<script>
import { defineAsyncComponent } from 'vue';
import HouseScene from './HouseScene.vue';

export default {
  name: 'HeaderContainer',
  components: {
    OptionsPopup: defineAsyncComponent(() =>
      import('@/components/OptionsPopup.vue')
    ),
    HouseScene,
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
      if(!this.config.show_house)  return false;
      return !this.config.minimal_mode;
    },
    getSettingsIconClass() {
      let cls = 'deactivated';
      if(this.showOptions)  cls = 'activated';
      return 'material-icon icon-settings icon-settings__' + cls;
    }
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