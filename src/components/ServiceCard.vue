<template>
  <div v-on:click="openLink" class="service-card-container">
    <h3>{{ title }}</h3>
    <img :src="iconPath">
    <div>{{subtitle}}</div>
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
