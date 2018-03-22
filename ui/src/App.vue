<template>
<div id="app-holder">
  <div id="sidebar">
      <a href="#">
          <img src="./assets/images/logo.png" id="logo" />
      </a>
      <hr class="hideable" />
      <ul>
          <li>
              <a href="http://cosmicpi.org/" target="_blank">
                  <i class="fa fa-wechat"></i>
                  <span class="hideable">Website <i class="fa fa-external-link"></i></span>
              </a>
              <hr />
          </li>
          <li>
              <router-link to="/">
                  <i class="fa fa-dashboard"></i>
                  <span class="hideable">Dashboard</span>
              </router-link>
          </li>
          <li>
              <router-link to="/settings">
                  <i class="fa fa-gears"></i>
                  <span class="hideable">Settings</span>
              </router-link>
          </li>
          <li>
              <router-link to="/about">
                  <i class="fa fa-info-circle"></i>
                  <span class="hideable">About</span>
              </router-link>
          </li>
      </ul>
      <hr class="hideable" />
      <p class="hideable" id="copyright">
          Copyright © Cosmic Pi Inc. 2018. <br />All Rights Reserved. <br />
      </p>
  </div>

  <div id="content" class="content">
        <router-view name="main"></router-view>
  </div>
</div>
</template>

<script>
export default {
  name: '',
}
</script>
