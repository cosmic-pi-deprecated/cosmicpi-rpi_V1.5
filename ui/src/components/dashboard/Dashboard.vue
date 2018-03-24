<template>
<div>
  <div class="row">
    <div class="col-6">
      <Histogram></Histogram>
    </div>
    <div class="col-6">
      <Location :longitude=lastLongitude :latitude=lastLatitude></Location>
    </div>
  </div>
  <div class="card-columns">
    <Value :value=lastTemperature icon="fa-thermometer-quarter" title="Temperature"></Value>
    <Value :value=lastHumidity icon="fa-thermometer-quarter" title="Humidity"></Value>
    <Value :value=lastPressure icon="fa-thermometer-quarter" title="Pressure"></Value>

    <Value :value=lastAcceleration icon="fa-tachometer" title="Acceleration"></Value>
    <Value :value=lastMagnet icon="fa-compass" title="Magnet"></Value>
    <Value :value=detectorInfo icon="fa-info-circle" title="Info"></Value>
    <Value :value=lastLocation icon="fa-map-marker" title="Location"></Value>
  </div>
</div>
</template>

<script>
import Value from './Value.vue';
import TimeSeries from './TimeSeries.vue';
import Location from './Location.vue';
import Histogram from './Histogram.vue';

export default {
  name: 'Dashboard',
  components: { Value, Histogram, Location },
  computed: {
    times() {
      return this.$store.getters.getTimeSeries();
    },
    lastTemperature() {
      return this.$store.getters.getLastValue('TemperatureC');
    },
    lastHumidity() {
      let value = this.$store.getters.getLastValue('Humidity');
      return (!isNaN(value)) ? value.toFixed(2) : value;
    },
    lastAcceleration() {
      let x = this.$store.getters.getLastValue('AccelX');
      let y = this.$store.getters.getLastValue('AccelY');
      let z = this.$store.getters.getLastValue('AccelZ');
      x = (!isNaN(x)) ? x.toFixed(3) : x;
      y = (!isNaN(x)) ? y.toFixed(3) : y;
      z = (!isNaN(x)) ? z.toFixed(3) : z;
      return `${x}\n${y}\n${z}`;
    },
    lastMagnet() {
      let x = this.$store.getters.getLastValue('MagX');
      let y = this.$store.getters.getLastValue('MagY');
      let z = this.$store.getters.getLastValue('MagZ');
      x = (!isNaN(x)) ? x.toFixed(4) : x;
      y = (!isNaN(x)) ? y.toFixed(4) : y;
      z = (!isNaN(x)) ? z.toFixed(4) : z;
      return `${x}\n${y}\n${z}`;
    },
    lastLocation() {
      let long = this.$store.getters.getLastValue('Longitude');
      let lati = this.$store.getters.getLastValue('Latitude');
      long = (!isNaN(long)) ? long.toFixed(6) : long;
      lati = (!isNaN(lati)) ? lati.toFixed(6) : lati;
      return `${long}\n${lati}`;
    },
    lastLongitude() {
      return this.$store.getters.getLastValue('Longitude');
    },
    lastLatitude() {
      return this.$store.getters.getLastValue('Latitude');
    },
    lastPressure() {
      let value = this.$store.getters.getLastValue('Pressure');
      return (!isNaN(value)) ? value.toFixed(0) : value;
    },
    detectorInfo() {
      let name = this.$store.getters.getLastValue('DetectorName');
      let version = this.$store.getters.getLastValue('DetectorVersion');
      let serial = this.$store.getters.getLastValue('HardwareSerial');
      return `${name}\n${version}\n${serial}`;
    },
  },
  beforeCreate() {
    this.$store.dispatch('requestSeries');

    setInterval(function() {
      this.$store.dispatch('requestSeries');
    }.bind(this), 5000); 
  },
}
</script>
