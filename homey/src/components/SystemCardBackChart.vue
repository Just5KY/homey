<template>
  <div class="system-card-back-chart-container">

    <div v-for="d in chartData.disks" :key="d.label" 
        class="system-card-back-chart-container__panel">
        <div class="system-card-back-chart-container__panel--details">
            <h3>{{ d.label }}</h3>
        </div>
        <div class="chart-container">
            <BarChart :chartData="diskChartData(d)" :options="config"/>
            <!-- <div class="chart-container__label">{{Math.floor(this.chartData.ram.percent_used)}}%</div> -->
        </div>
    </div>

  </div>
</template>

<script>
    import { BarChart } from 'vue-chart-3';
    import Chart from 'chart.js/auto';

    export default {
        name: 'SystemCardBackChart',
        components: {
            BarChart
        },
        props: {
            chartData: Object,
        },
        data: function() {
            return {
                config: {
                    indexAxis: 'y',
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
                            stacked: true,
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
                    }
                }
            }
        },
        methods: {
            diskChartData(disk) {
                return  {
                    labels: [disk.label],
                    datasets: [{
                        borderWidth: 0,
                        borderRadius: 7.5,
                        borderSkipped: false,
                        maxBarThickness: 34,
                        backgroundColor: ['#8be9fd'],
                        label: disk.label,
                        data: [ disk.used ],
                    },
                    {
                        borderWidth: 0,
                        borderRadius: 7.5,
                        borderSkipped: false,
                        maxBarThickness: 34,
                        backgroundColor: ['rgba(248, 248, 242, .1)'],
                        label: disk.label,
                        data: [ disk.free ],
                    }]
                };
            },
        },
        computed: {
            
        },
        mounted() {
        }
    }
</script>