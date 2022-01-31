<template>
  <div class="system-card-back-chart-container">

    <div v-for="d in chartData.disks" :key="d.label"
        :title="getDiskInfo(d)"
        class="system-card-back-chart-container__panel">
        <div class="system-card-back-chart-container__panel--details">
            <h3>{{ d.label }}</h3>
            <p>{{ d.free }}GB free</p>
        </div>
        <div class="back-chart-container">
            <BarChart :chartData="diskChartData(d)" :options="config"/>
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
                    reactive: true,
                    maintainAspectRatio: false,
                    layout: {
                        padding: {
                            left: -10,
                            bottom: -10,
                        },
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
                        tooltip: { enabled: false },
                        legend: { display: false },
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
                        borderRadius: 5,
                        borderSkipped: false,
                        barPercentage: 1,
                        categoryPercentage: 1,
                        backgroundColor: ['#8be9fd'],
                        label: disk.label,
                        data: [ disk.percent_used ],
                    },
                    {
                        borderWidth: 0,
                        borderRadius: 5,
                        borderSkipped: false,
                        barPercentage: 1,
                        categoryPercentage: 1,
                        backgroundColor: ['rgba(248, 248, 242, .1)'],
                        label: disk.label,
                        data: [ 100 ],
                    }]
                };
            },
            getDiskInfo(disk){
                return 'Label: ' + disk.label + '\nTotal size: ' + disk.total 
                    + 'GB\nUsed: ' + disk.used + 'GB (' + disk.percent_used 
                    + '%) \nFree: ' + disk.free + 'GB (' + (100 - disk.percent_used) + '%)'
            }
        },
        computed: {
            
        },
        mounted() {
        }
    }
</script>