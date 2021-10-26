<template>
    <div class="api-card">
        <p>API request to {{this.url}}</p>
    </div>
</template>

<script>

export default {
    name: "APICard",
    props: {
        url: String,
        //icon: String,
    },
};

</script>

<style scoped>

.api-card{
    border: 2px solid black;
    width: 50%;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem auto 1rem auto;
}

.api-card > p {
    font-size: 2rem;
    color: bisque;
}


</style>