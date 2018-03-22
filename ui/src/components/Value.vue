<template>
  <div class="col-bg-3 col-md-4 col-sm-6 col-xs-12 item">
    <div class="card card-default bg-primary">
      <div class="card-body">
        <div class="row">
          <div class="col-3">
            <i :class="[ ['fa', icon, 'fa-5x'].join(' ') ]"></i>
          </div>
          <div class="col-9 text-right">
            <div class="huge">{{ value }}</div>
            <div class="card-title">{{ title }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Value',
  props: ['value', 'icon', 'title'],
}
</script>

<style>
.item {
  padding-bottom: 20px;
}
</style>