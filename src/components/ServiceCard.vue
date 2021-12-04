<template>
  <div class="service-card-container">
    <h3>{{ title }}</h3>
    <img :src="iconPath">
    <div>{{subtitle}}</div>
    <div>{{url}}</div>
  </div>
</template>

<script>
import { computed } from '@vue/reactivity'
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
}
</script>
