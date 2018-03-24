<template>
<div class="row">
    <div class="col-md-8 offset-md-2 col-sm-12 box">
        <h3>Export Data</h3>
        <hr />
        <div class="row">
            <div class="form-group col">
                <label for="fromDate">From date:</label>
                <datetime @input="rangeUpdated" v-model="from" id="fromDate" type="datetime" input-class="form-control"></datetime>
            </div>
            <div class="form-group col">
                <label for="toDate">To date:</label>
                <datetime @input="rangeUpdated" v-model="to" id="toDate" type="datetime" input-class="form-control"></datetime>
            </div>
        </div>
        <div class="row">
            <img ref="graph" style="width: 100%; height: 100%" />
        </div>
                
        <div class="row">
            <div class="col">
                <a href="#" target="_blank" ref="csvButton" class="btn btn-primary btn-block">Download CSV</a>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import { Datetime } from 'vue-datetime'
import moment from 'moment';


const FROM_DEFAULT = moment().add('-24', 'hours').toISOString();
const TO_DEFAULT = moment().toISOString();

export default {
    name: 'Science',
    data() {
        return {
            from: FROM_DEFAULT,
            to: TO_DEFAULT,
            lastFrom: FROM_DEFAULT,
            lastTo: TO_DEFAULT,
        }
    },
    components: {
        Datetime: Datetime
    },
    mounted() {
        this.loadGraphImage();
        this.updateDownloadUrl();
    },
    methods: {
        rangeUpdated() {
            if (this.lastFrom != this.from || this.lastTo != this.to) {
                this.lastFrom = this.from;
                this.lastTo = this.to;

                this.loadGraphImage();
                this.updateDownloadUrl();
            }
        },
        updateDownloadUrl() {
            let from = moment(this.from).unix();
            let to = moment(this.to).unix();
            let root = this.$http.options.root;

            let url = `${root}series?format=csv&from=${from}&to=${to}`;
            this.$refs.csvButton.href = url;
        },
        loadGraphImage() {
            let from = moment(this.from).unix();
            let to = moment(this.to).unix();
            let root = this.$http.options.root;
            let binSize = 1;

            let imageUrl = `${root}histogram.png?from=${from}&to=${to}&bin_size=${binSize}`;
            this.$refs.graph.src = imageUrl;
        },
    },
}
</script>