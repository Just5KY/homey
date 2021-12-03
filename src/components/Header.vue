<template>
  <div class="header-container">
    <h1>{{ title }}<span class="material-icons-outlined">settings</span></h1>
    <canvas class="webgl"></canvas>
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