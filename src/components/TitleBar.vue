<template>
    <div id="title-bar">
        <h1>{{this.title}}</h1>
        <span id="title-info-container">
            <div class="title-info-element">{{this.formattedTime}}</div>
            <div class="title-info-element">{{this.formattedDate}}</div>
            <div class="title-info-element">72 // Cloudy</div>
        </span>
    </div>
</template>

<script>

export default {
    name: "TitleBar",
    props: {
        title: String,
    },
    data: function() {
        return {
            formattedTime: String,
            formattedDate: String,
        };
    },
    methods: {
        updateTime(){
            this.formattedTime = new Date().toLocaleTimeString();
        },
        updateDate(){
            this.formattedDate = new Date().toLocaleDateString();
        }
    },
    mounted() {
        this.updateTime();
        this.updateDate();

        setInterval(() => this.updateTime(), 1000);
        setInterval(() => this.updateDate(), 1000 * 60 * 2); // update date every 2 minutes
    },
}
</script>

<style scoped>

#title-bar {
    text-align: left;
}

h1 {
    width: 60%;
    display: inline-block;
}

#title-info-container {
    margin-left: auto;
    margin-right: 0;
    text-align: right;
    width: 40%;
    display: inline-block;
}

.title-info-element {
    margin-left: auto;
    margin-right: 0;
    
}

</style>