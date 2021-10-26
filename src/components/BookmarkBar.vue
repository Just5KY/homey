<template>
    <button id="toggle-button" @click=toggleHidden>Toggle Bookmarks</button>
    <ul v-if="!this.hidden" id="bookmark-bar">
        <a class="bookmark-link" target="_blank" :href="b.url" v-for="b in bookmarkList" :key=b.name>{{b.name}}</a>
    </ul>
</template>

<script>
export default {
    name: 'BookmarkBar',
    props: {
        bookmarkList: Array,
    },
    data: function() {
        return {
            hidden: false,
        }
    },
    methods: {
        toggleHidden() {
            if(this.hidden){
                this.hidden = false;
                return;
            }
            this.hidden = true;
        }
    },
}
</script>

<style>
#bookmark-bar{
    border: 1px solid black;
    width: 50%;
    margin: auto;
    padding: 0.5rem;
}

.bookmark-link {
    font-size: 1rem;
    color: bisque;
    padding: 1rem;
}
</style>