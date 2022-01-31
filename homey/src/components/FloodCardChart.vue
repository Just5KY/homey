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
                    interaction: {
                        mode: "index",
                        intersect: false,
                    },
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
                        },
                        tooltip: {
                            position: 'nearest',
                            backgroundColor: 'rgba(40, 42, 54, .8)',
                            titleColor: '#f8f8f2',
                            bodyColor: '#f8f8f2',
                            titleFont: {
                                family: 'Montserrat'
                            },
                            bodyFont: {
                                family: 'Montserrat'
                            },
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    label += ': '

                                    if (context.parsed.y > Math.pow(2, 30))  
                                        label += Math.floor(context.parsed.y / 100000).toString() + 'gb/s';
                                    else if (context.parsed.y > Math.pow(2, 20))
                                        label += Math.floor(context.parsed.y / 10000).toString() + 'mb/s';
                                    else if (context.parsed.y > Math.pow(2, 10))
                                        label += Math.floor(context.parsed.y / 1000).toString() + 'kb/s';
                                    else label += Math.floor(context.parsed.y).toString() + ' b/s'

                                    return label;
                                }
                            }
                        },
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
                            label: 'Up', 
                            data: upData, 
                            borderColor: '#8be9fd', backgroundColor: '#8be9fd', 
                            pointRadius: 0, 
                            tension: .15, 
                            fill: false,
                            order: this.getDrawOrder.up
                        }, 
                        { 
                            label: 'Down', 
                            data: downData, 
                            borderColor: '#f8f8f2', backgroundColor: '#f8f8f2', 
                            pointRadius: 0, 
                            tension: .15, 
                            fill: false, 
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