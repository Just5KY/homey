<template>
  <div v-on:click="openLink" class="service-card-container">
    <div class="service-card-container__text-container">
      <h3>{{ title }}</h3>
      <div class="service-card-container__subtitle">{{subtitle}}</div>
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
  },
  methods: {
    openLink: function() {
      window.open(this.url,'_blank');
    }
  }
}
</script>
