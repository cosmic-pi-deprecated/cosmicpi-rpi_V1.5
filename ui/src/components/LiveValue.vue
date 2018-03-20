<template>
    <div class="card bg-primary col-bg-3 col-md-4 col-sm-6 col-xs-12">
      <div class="card-body">
        <div class="row">
          <div class="col-3">
            <i class="fa fa-thermometer-quarter fa-5x"></i>
          </div>
          <div class="col-9 text-center">
            <div class="huge">{{ value }}</div>
            <div class="card-title">Temperature</div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: 'LiveValue',
  props: ['value', 'icon'],
}
</script>