<template>
  <LineChart :chartData="newChartData" :options="config"/>
</template>

<script>
    //import { Line } from 'vue-chartjs'
    import { LineChart } from 'vue-chart-3';
    import Chart from 'chart.js/auto';

    export default {
        name: 'FloodCardChart',
        //extends: Line,
        //props: ['data', 'options'],
        components: {
            LineChart,
        },
        props: {
            chartData: Array,
        },
        data: function() {
            return {
                config: {
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
                        { label: 'Upload', data: upData, borderColor: '#8be9fd', pointRadius: 0, tension: .15 }, 
                        { label: 'Download', data: downData, borderColor: '#f8f8f2', pointRadius: 0, tension: .15 } 
                    ], 
                };
            }
        },
        mounted() {
        }
    }
</script>