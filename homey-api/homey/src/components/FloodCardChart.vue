<template>
  <LineChart :chartData="newChartData" :options="config"/>
</template>

<script>
    import { LineChart } from 'vue-chart-3';
    import Chart from 'chart.js/auto';

    export default {
        name: 'FloodCardChart',
        components: {
            LineChart,
        },
        props: {
            chartData: Array,
        },
        data: function() {
            return {
                config: {
                    responsive: true,
                    scales: {
                        x: {
                            ticks: { display: false},
                            grid: {
                                display: false,
                                drawBorder: false
                            }
                        },
                        y: {
                            ticks: { display: false},
                            grid: {
                                display: false,
                                drawBorder: false
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false,
                        }
                    }
                }
            }
        },
        computed: {
            newChartData: function() {
                let upData = []
                let downData = []
                let timeLabels = []
                this.chartData.forEach(c => {
                    upData.push(c.up);
                    downData.push(c.down);
                    timeLabels.push(c.time);
                });
                return { 
                    labels: timeLabels,
                    datasets: [ 
                        { 
                            label: 'Upload', 
                            data: upData, 
                            borderColor: '#8be9fd', backgroundColor: '#8be9fd', 
                            pointRadius: 0, 
                            tension: .15, 
                            fill: true,
                            order: this.getDrawOrder.up
                        }, 
                        { 
                            label: 'Download', 
                            data: downData, 
                            borderColor: '#f8f8f2', backgroundColor: '#f8f8f2', 
                            pointRadius: 0, 
                            tension: .15, 
                            fill: true, 
                            order: this.getDrawOrder.down
                        } 
                    ], 
                };
            },
            getDrawOrder: function() {
                if(this.chartData[this.chartData.length-1].up > this.chartData[this.chartData.length-1].down){
                    return {up: 1, down: 0}
                }
                return {up: 0, down: 1}
            }
        },
        mounted() {
        }
    }
</script>