<template>
  <div v-on:click="openLink" class="service-card-container">
    <div class="service-card-container__text-container">
      <h3>{{ title }} 
        <span v-if="displayStatus" :title="getStatusFormatted" :id="getStatus" class="service-card-container__text-container__indicator material-icons-outlined">{{ getStatus }}</span>
      </h3>
      <div class="service-card-container__text-container__subtitle">{{subtitle}}
      </div>
    </div>
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
      iconPath: "./images/icons/" + this.icon,
    };
  },
  props: {
      title: String,
      subtitle: String,
      icon: String,
      url: String,
      displayStatus: Boolean,
      isUp: Boolean,
  },
  computed: {
    getStatus: function() {
      if(this.isUp) return 'arrow_upward';
      return 'arrow_downward';
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
