<template>
  <div class="header-container">
    <canvas class="header-animation"></canvas>
    <h1>{{ title }}</h1>
    <span @click="showOptions = !showOptions" class="material-icons-outlined">settings</span>
    <transition name="modal">
      <OptionsPopup v-if="showOptions" @close="showOptions = false" tabindex="0" @keydown.esc="showOptions = false"/>
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
    title: String
  },
  data: function() {
    return {
      showOptions: false,
    };
  }
}
</script>