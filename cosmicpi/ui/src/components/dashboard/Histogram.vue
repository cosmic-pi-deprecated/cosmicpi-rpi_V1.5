<template>
<div class="card card-default card-margin">
    <div class="card-header">
        <h5>Histogram</h5>
        <div class="row">
            <div class="col-sm-9 col-md-10">
                <p class="small">
                    Showing data in period {{from}} - {{to}} ({{period}}s), 
                    <b>{{ numberOfEvents }}</b> events with
                    bin size <b>{{ binSize }}s</b>
                </p>
            </div>
            <div class="col-sm-3 col-md-2">
                <input v-model="binSize" class="form-control" min="1" type="number"/>
            </div>
        </div>
    </div>
    <div class="card-body card-narrow">
        <canvas ref="canvas" style="height:300px"></canvas>
    </div>
</div>
</template>

<script>
import Chart from 'chart.js';
import moment from 'moment';


const DEFAULT_BIN_SIZE = 1;


export default {
    name: 'Histogram',
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
                    // label: 'Number of events',
                    backgroundColor: "rgba(153,51,255,0.4)"
                }]
            },
            options: {
                animation: false,
                legend: {
                    display: false,
                },
                scales: {
                    xAxes: [{
                        display: false,
                        scaleLabel: {
                            display: true,
                            labelString: 'Time',
                        }
                    }],
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Number of events'
                        },
                        ticks: {
                            beginAtZero: true,
                            min: 0,
                            stepSize: 1
                        }
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
</style>
