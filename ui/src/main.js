import Vue from 'vue'
import router from './router.js'
import App from './App.vue'
import $ from 'jquery';
import './assets/css/main.css'
import '../node_modules/bootstrap/dist/css/bootstrap.css'
import '../node_modules/font-awesome/css/font-awesome.css'

window.jQuery = $;
window.$ = $;

new Vue({
    el: '#app',
    router,
    template: '<App/>',
    components: { App }
})
  
