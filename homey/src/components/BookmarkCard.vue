<template>
  <div class="bookmark-card-container">
      <div class="bookmark-card-container__side bookmark-card-container__side--front">
          <div class="bookmark-card-container__heading">
            <span class="material-icon icon-bookmarks bookmark-card-container__heading__icon"></span>
            <span class="bookmark-card-container__heading--title">Bookmarks</span>
          </div>
          <div class="bookmark-card-container__main">
            <ul>
              <li v-for="b in bookmarks" :key="b.name" class="bookmark"
                @click="openLink(b.url)" :title="b.hover">
                  <h3>{{b.name}}</h3>
                  <span class="material-icon icon-arrow_right bookmark__arrow"></span>
              </li>
            </ul>
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
    openLink(url) {
      window.open(url,'_blank');
    }
  },
}
</script>
