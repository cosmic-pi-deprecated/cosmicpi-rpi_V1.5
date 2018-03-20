<template>
<div class="row">
  <LiveValue value="NA" icon="fa-thermometer-quarter"></LiveValue>
</div>
</template>

<script>
import LiveValue from './LiveValue.vue'


export default {
  name: 'Dashboard',
  components: {
    LiveValue
  },
  data () {
    return {
      temperatureValue: 'NA',
    }
  },
}
</script>
