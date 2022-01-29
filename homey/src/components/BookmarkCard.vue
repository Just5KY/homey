<template>
  <div class="bookmark-card-container">
      <div class="bookmark-card-container__side bookmark-card-container__side--front">
          <div class="bookmark-card-container__heading">
            <span class="bookmark-card-container__heading--title">Bookmarks</span>
          </div>
          <div class="bookmark-card-container__main">
            <ul>
              <li v-for="b in bookmarks" :key="b.name"/>
            </ul>
          </div>
      </div>
      <div class="bookmark-card-container__side bookmark-card-container__side--back">
          <div class="bookmark-card-container__notifications">
            
          </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'BookmarkCard',
  props: {
      bookmarks: Array
  },
  data () {
    return {
      
    }
  },
  methods: {
    
  },
}
</script>
