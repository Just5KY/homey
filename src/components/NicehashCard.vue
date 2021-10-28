<template>
    <div class="api-card" id="nicehash-card">
        <h3>{{this.name}}</h3>
        <p>{{this.message}}</p>
    </div>
</template>

<script>

//import Api from '../assets/js/api.js'
//import config from '../assets/js/config.js'
//const api = new Api(config);

//const axios = require('axios').default;

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
            /*
            api.getTime()
            .then(() => {
                console.log('server time', api.time)
                console.log('--')
            })

            // get balance
            
            .then(() => api.get('/main/api/v2/accounting/accounts2'))
            .then(res => {
                console.log('accounts', res);
            })
            // get live miner stats
            .then(() => api.get('/main/api/v2/mining/algo/stats'))
            .then(res => {
                console.log('algorithms', res);
            })
            

            .catch(err => {
                if(err && err.response) console.log(err.response.request.method,err.response.request.uri.href);
                console.log('ERROR', err.error || err);
            }) */
            
            //axios.get('https://api2.nicehash.com/api/v2/time')
                //.then(response => (this.message = response.data[0]['serverTime']));
        },
    },
    mounted () {
        this.message = "Loading..."
        this.fetchData();
        
        if(this.refreshInterval == 0)   return;
        setInterval(() => this.fetchData(), this.refreshInterval * 1000);
    },
};

</script>

<style scoped>

</style>