<template>
<div class="card card-default bg-light">
  <div class="card-body">
    <div class="row">
      <div class="col-3">
        <i :class="[ ['fa', icon, 'fa-5x'].join(' ') ]"></i>
      </div>
      <div class="col-9 text-right">
        <pre class="huge">{{ value }}</pre>
        <div class="card-title">{{ title }}</div>
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
.huge {
  font-size: 24px;
}
</style>