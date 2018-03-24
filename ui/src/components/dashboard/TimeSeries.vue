<template>
<div class="card card-default">
    <div class="card-header">
        <h5>{{ title }}</h5>
    </div>
    <div class="card-body">
        <canvas ref="canvas" style="height:300px"></canvas>
    </div>
</div>
</template>

<script>
import Chart from 'chart.js'


export default {
    name: 'TimeSeries',
    props: ['title', 'dkey'],
    data() {
        return {
            chart: null,
        }
    },
    computed: {
        times() {
            return this.$store.getters.getTimeSeries();
        },
        values() {
            return this.$store.getters.getSeries(this.dkey);
        }
    },
    watch: {
        'times': function() { 
            this.chart.data.datasets[0].data = this.values;
            this.chart.data.labels = this.times
            this.chart.update();
         }
    },
    mounted() {
        this.chart = new Chart(this.$refs.canvas, {
            type: 'line',
            data: {
                labels: this.times,
                datasets: [{
                    label: this.title,
                    data: this.values,
                    backgroundColor: "rgba(153,51,255,0.4)"
                }]
            },
            options: {
                animation: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [{
                        display: false
                    }]
                },
            },
        });

        /*
        setInterval(() => {
            this.$store.dispatch('addRandomValues');
        }, 1000);
        */
    },
}
</script>

<style>
.card {
    margin-bottom: 20px;
}
</style>
