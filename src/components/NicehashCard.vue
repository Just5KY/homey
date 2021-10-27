<template>
    <div class="api-card" id="nicehash-card">
        <h3>{{this.name}}</h3>
        <p>{{this.message}}</p>
    </div>
</template>

<script>

const axios = require('axios').default;
axios.defaults.withCredentials = false;

export default {
    name: "NicehashCard",
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
            //axios.get(this.url)
                //.then(response => (this.message = response.data[0]['q'] + ' - ' + response.data[0]['a']));
        },
    },
    mounted () {
        this.message = "Loading..."
        this.fetchData();
        setInterval(() => this.fetchData(), this.refreshInterval * 1000);
    },
};

</script>

<style scoped>

</style>