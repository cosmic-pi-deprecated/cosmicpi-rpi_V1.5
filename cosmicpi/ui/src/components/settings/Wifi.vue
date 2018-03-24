<template>
<div class="col-md-6 offset-md-3 col-sm-8 offset-sm-2 ">
    <div class="card card-default">
        <div class="card-header">
            <h3>Wifi</h3>
        </div>

        <div class="card-body">
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
    </div>
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
