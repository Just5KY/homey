<template>
    <div class="api-card">
        <h3>{{this.name}}</h3>
        <p>{{this.message}}</p>
    </div>
</template>

<script>

const axios = require('axios').default;
axios.defaults.withCredentials = false;

export default {
    name: "APICard",
    props: {
        name: String,
        url: String,
        refreshInterval: Number,    // In seconds. 0 = do not refresh
        //icon: String,
    },
    data: function() {
        return {
            message: String,
        }
    },
    methods: {
        fetchData() {
            axios.get(this.url)
                .then(response => (this.message = response.data[0]['q'] + ' - ' + response.data[0]['a']));
        },
    },
    mounted () {
        this.fetchData();
        setInterval(() => this.fetchData(), this.refreshInterval * 1000);
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