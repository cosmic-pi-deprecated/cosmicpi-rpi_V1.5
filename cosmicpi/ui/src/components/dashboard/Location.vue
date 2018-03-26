<template>
<div class="card card-default card-margin">
    <div class="card-header">
        <h5>Location</h5>
    </div>
    <div class="card-body card-narrow">
        <iframe class="google-map" ref="map" :src=googleMapsUrl></iframe>
    </div>
</div>
</template>

<script>
const MAPS_KEY = 'AIzaSyBjX-IrwBEp7lncv8Q-OXsY549c5zNh_kY';

export default {
    name: 'Location',
    props: ['latitude', 'longitude'],
    data() {
        return {
            chart: null,
        }
    },
    computed: {
        googleMapsUrl() {
            return `https://www.google.com/maps/embed/v1/place?q=${this.latitude},${this.longitude}&key=${MAPS_KEY}`;
        },
    },
}
</script>

<style>
.google-map {
    width: 100%;
    height: 300px;
    border: 0;
}
</style>

