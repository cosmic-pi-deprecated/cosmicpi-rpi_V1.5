<template>
<div class="card card-default">
    <div class="card-header">
        <h5>Histogram</h5>
        <p class="small">
            Showing data in period {{from}} - {{to}} ({{period}}s), 
            <b>{{ numberOfEvents }}</b> events with
            bin size <b>{{ binSize }}s</b>
        </p>
    </div>
    <div class="card-body">
        <canvas ref="canvas" style="height:300px"></canvas>
    </div>
    <div class="card-footer">
        <input v-model="binSize" class="form-control" min="1" type="number"/>
    </div>
</div>
</template>

<script>
import Chart from 'chart.js';
import moment from 'moment';


const DEFAULT_BIN_SIZE = 1;


export default {
    name: 'Histogram',
    props: ['title', 'dkey'],
    data() {
        return {
            chart: null,
            binSize: DEFAULT_BIN_SIZE,
        }
    },
    computed: {
        times() {
            return this.$store.getters.getSeries('UTCUnixTime');
        },
        from() {
            return moment(this.times[0] * 1000).format('LLL');
        },
        to() {
            return moment(this.times[this.times.length - 1] * 1000).format('LLL');
        },
        numberOfEvents() {
            return this.$store.getters.getNumberOfEvents();
        },
        period() {
            return moment.duration(this.$store.getters.getPeriod() * 1000).asSeconds();
        },
    },
    watch: {
        'binSize': function() { this.generateGraph() },
        'times': function() { this.generateGraph() },
    },
    methods: {
        generateGraph() {
            let list = this.times;

            // Create histogram
            let histogram = {}
            list = list.map(x => x - (x - list[0]) % this.binSize);
            list.forEach(x => histogram[x] = (histogram[x] || 0) + 1);

            // Put histogram in chart
            this.chart.data.datasets[0].data = Object.values(histogram);
            this.chart.data.labels = Object.keys(histogram).map(x => moment(x * 1000).format('MMMM DD, YYYY HH:mm:ss'))
            this.chart.update();
        },
    },
    mounted() {
        this.chart = new Chart(this.$refs.canvas, {
            type: 'bar',
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
    },
}
</script>

<style>
.small {
    font-size: 12px;
}

.card {
    margin-bottom: 20px;
}
</style>
