<template>
  <a :href="url" target="_blank" :class="getClass" rel="noopener noreferrer">
    <div class="service-card-container__text-container">
      <h3>{{ title }}</h3>
      <div v-if="subtitle && subtitle != ''" class="service-card-container__text-container__subtitle">{{subtitle}}</div>
    </div>
    <div class="service-card-container__indicator">
      <transition name="modal-fade">
        <span v-if="displayStatus" :title="getStatusFormatted" :id="getStatus + ((isCompact) ? '__compact' : '')" 
          :class="'service-card-container__indicator--icon material-icon ' + getStatus"></span>
      </transition>
    </div>
    <div class="service-card-container__image-container">
      <img :src="iconPath" onerror="this.onerror=null; this.src='data/icons/default.png?t=' + new Date().getTime()">
    </div>
  </a>
</template>

<script>
export default {
  name: 'ServiceCard',
  data: function () {
    return {
      iconPath: "./data/icons/" + this.icon,
    };
  },
  props: {
      title: String,
      subtitle: String,
      icon: String,
      url: String,
      displayStatus: Boolean,
      isUp: Boolean,
      isCompact: Boolean,
  },
  computed: {
    getClass() {
      return ((this.isCompact) ? 'service-card-container service-card-container__compact' : 'service-card-container')
    },
    getStatus: function() {
      if(this.isUp) return 'icon-arrow_up';
      return 'icon-arrow_down';
    },
    getStatusFormatted: function() {
      return this.title + ' is ' + ( (this.isUp) ? '' : 'un' ) + 'reachable at ' + this.url
    }
  },
  methods: {
    openLink: function() {
      window.open(this.url,'_blank');
    }
  },
}
</script>
