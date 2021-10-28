<template>
    <div id="title-bar">
        <h1>{{this.title}}</h1>
        <div id="title-info-container">
            <div>{{this.formattedTime}}</div>
            <div>{{this.formattedDate}}</div>
            <div>72 // Cloudy</div>
        </div>
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



#title-info-container {
    margin-left: auto;
    margin-right: 0;
}

</style>