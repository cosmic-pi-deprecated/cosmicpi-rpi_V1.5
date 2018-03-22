<template>
<div class="row">
  <Value :value=lastTemperature icon="fa-thermometer-quarter" title="Temperature"></Value>
  <Value :value=lastHumidity icon="fa-thermometer-quarter" title="Humidity"></Value>

  <TimeSeries title="Temperature (C)" dkey="TemperatureC"></TimeSeries>
</div>
</template>

<script>
import Value from './Value.vue'
import TimeSeries from './TimeSeries.vue'

export default {
  name: 'Dashboard',
  components: { Value, TimeSeries },
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
  },
  beforeCreate() {
    this.$store.dispatch('requestSeries');
  },
}
</script>
