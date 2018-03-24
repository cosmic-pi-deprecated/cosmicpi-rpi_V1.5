<template>
<div class="col-md-4 offset-md-4 col-sm-6 offset-sm-4 box">
    <h3 class="text-center">Wifi</h3>
    <hr />
    <div v-if="connected" class="alert alert-success">
        Great, you are already connected to wifi network <b>{{ currentWifi }}</b>!
    </div>
    <div v-if="response" class="alert alert-warning">
        {{ response }}
    </div>

    <form @submit.prevent="onFormSubmit">
        <div class="form-group">
            <label for="inputSSID">SSID:</label>
            <select class="form-control" ref="ssid" id="inputSSID">
                <option v-for="wifi in wifiList" :key="wifi" :value="wifi">{{ wifi }}</option>
            </select>
        </div>
        <div class="form-group">
            <label for="inputPassword">Password</label>
            <input type="password" ref="pass" class="form-control" id="inputPassword">
        </div>
        <button type="submit" ref="submit" class="btn btn-primary btn-lg btn-block">Connect</button>
    </form>
</div>
</template>

<script>
import Vue from 'vue';


export default {
    name: 'Wifi',
    data() {
        return {
            response: '',
        }
    },
    computed: {
        wifiList() {
            return this.$store.getters.getWifiList();
        },
        currentWifi() {
            return this.$store.getters.getCurrentWifi();
        },
        connected() {
            return this.currentWifi.length > 0;
        }
    },
    methods: {
        enable(enabled) {
            this.$refs.ssid.disabled = !enabled;
            this.$refs.pass.disabled = !enabled;
            this.$refs.submit.disabled = !enabled;
        },
        onFormSubmit() {
            let wifiDetails = {
                ssid: this.$refs.ssid.value,
                pass: this.$refs.pass.value,
            };
            let params = {
                token: this.$store.getters.getToken(),
            };
            this.enable(false);
            Vue.http.post('wifi', wifiDetails, { params, emulateJSON: true, }).then(response => {
                this.response = response.body.message;
            });
        }
    },
    created() {
        this.$store.dispatch('requestWifi');
    },
}
</script>

<style>
.box {
    border: 1px solid #ddd;
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 5px; 
}
</style>
