<template>
  <div v-on:click="openLink" :class="getClass">
    <div class="service-card-container__text-container">
      <h3>{{ title }}</h3>
      <div class="service-card-container__text-container__subtitle">{{subtitle}}
      </div>
    </div>
    <span v-if="displayStatus" :title="getStatusFormatted" :id="getStatus + ((isCompact) ? '__compact' : '')" :class="'service-card-container__indicator material-icon ' + getStatus"></span>
    <div class="service-card-container__image-container">
      <img :src="iconPath">
    </div>
  </div>
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
