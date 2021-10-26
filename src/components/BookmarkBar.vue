<template>
    <ul id="bookmark-bar">
        <a class="bookmark-link" target="_blank" :href="b.url" v-for="b in bookmarkList" :key=b.name>{{b.name}}</a>
    </ul>
</template>

<script>
export default {
    name: 'BookmarkBar',
    props: {
        bookmarkList: []
    },
    data: function() {
        return {
            hidden: false,
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