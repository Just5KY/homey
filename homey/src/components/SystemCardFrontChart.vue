<template>
  <div class="system-card-front-chart-container">

    <div class="system-card-front-chart-container__panel">
        <div class="front-chart-container">
            <DoughnutChart :chartData="cpuChartData" :options="config" :plugins="[backgroundPlugin]"/>
            <div class="front-chart-container__label">{{Math.floor(this.chartData.cpu)}}%</div>
        </div>
        <div class="system-card-front-chart-container__panel--details">
            <h3>CPU</h3>
        </div>
    </div>

    <div class="system-card-front-chart-container__panel"
        :title="getMemoryInfo">
        <div class="front-chart-container">
            <DoughnutChart :chartData="memoryChartData" :options="config" :plugins="[backgroundPlugin]"/>
            <div class="front-chart-container__label">{{Math.floor(this.chartData.ram.percent_used)}}%</div>
        </div>
        <div class="system-card-front-chart-container__panel--details">
            <h3>RAM</h3>
        </div>
    </div>

  </div>
</template>

<script>
import { DoughnutChart } from 'vue-chart-3';
import Chart from 'chart.js/auto';



export default {
    name: 'SystemCardFrontChart',
    extends: DoughnutChart,
    components: {
        DoughnutChart
    },
    props: {
        chartData: Object,
    },
    data: function() {
        return {
            backgroundPlugin: {
                id: 'custom_canvas_background_color',
                beforeDraw: (chart) => {
                    const ctx = chart.canvas.getContext('2d');
                    const center = chart.canvas.height / 2;

                    ctx.beginPath();
                    ctx.arc(center, center, center - 10, 0, 2 * Math.PI, false);
                    ctx.lineWidth = 20;
                    ctx.strokeStyle = 'rgba(248, 248, 242, .1)';
                    ctx.stroke();
                }
            },
            config: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false,
                    },
                    tooltip: {
                        enabled: false,
                    },
                    
                }
            }
        }
    },
    computed: {
        cpuChartData() {
            return  {
                labels: ['CPU', 'a'],
                datasets: [{
                    borderWidth: 0,
                    borderRadius: 5,
                    backgroundColor: ['#f8f8f2', 'transparent'],
                    label: 'CPU',
                    data: [ this.chartData.cpu, 100 - this.chartData.cpu ],
                }]
            };
        },
        memoryChartData() {
            return  {
                labels: ['RAM'],
                datasets: [{
                    borderWidth: 0,
                    borderRadius: 5,
                    backgroundColor: ['#f8f8f2', 'transparent'],
                    label: 'RAM',
                    data: [ this.chartData.ram.percent_used, 100 - this.chartData.ram.percent_used ],
                }]
            };
        },
        getMemoryInfo() {
            return 'Total: ' + Math.floor(this.chartData.ram.total / 1000) + 'GB\n' +
                'Free: ' + Math.floor(this.chartData.ram.free / 1000) + 'GB\n' +
                'Used: ' + this.chartData.ram.used + 'MB (' + Math.floor(this.chartData.ram.percent_used) + '%)'
        }
    },
    mounted() {
    }

}
</script>