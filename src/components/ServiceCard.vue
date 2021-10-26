<template>
    <div class="card">
        <a :href=this.url target="_blank">{{this.name}}</a>
        <img :src="'../assets/icons/' + icon">
    </div>
</template>

<script>

export default {
    name: "ServiceCard",
    props: {
        name: String,
        url: String,
        icon: String,
    },
    computed: {
        getIconPath() {
            return '../assets/image'
        }
    },
};

</script>

<style scoped>

.card{
    border: 2px solid black;
    width: 50%;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem auto 1rem auto;
}

.card > a {
    font-size: 2rem;
    color: bisque;
}

.card > img {
    width: 3rem;
}

</style>