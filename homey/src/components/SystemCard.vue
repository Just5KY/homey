<template>
  <div :class="getClass" @click="isFlipped = !isFlipped" @mouseleave="isFlipped = false">
      <div class="system-card-container__side system-card-container__side--front">
          <div class="system-card-container__heading">
            <span class="material-icons-outlined system-card-container__heading__icon">query_stats</span>
            <span class="system-card-container__heading--title">System</span>
          </div>
          <div class="system-card-container__main">
            
          </div>
      </div>
      <div class="system-card-container__side system-card-container__side--back">
          <div class="system-card-container__notifications">
            
          </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'SystemCard',
  props: {
      
  },
  computed: {
    getClass() {
      return 'system-card-container' + ((this.isFlipped) ? ' system-card-container__flipped' : '' )
    },
  },
  data () {
    return {
      isFlipped: false,
    }
  },
  methods: {
    
  },
}
</script>
