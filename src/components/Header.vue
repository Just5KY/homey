<template>
  <div class="header-container">
    <canvas class="header-animation"></canvas>
    <h1>{{ title }}</h1>
    <span class="material-icons-outlined">settings</span>
  </div>
</template>

<script>
export default {
  name: 'Header',
  props: {
    title: String
  }
}
</script>