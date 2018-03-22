import Vue from 'vue'
import VueResource from 'vue-resource';
import router from './router.js'
import store from './store.js';
import App from './App.vue'
import './assets/css/main.css'
import '../node_modules/bootstrap/dist/css/bootstrap.css'
import '../node_modules/font-awesome/css/font-awesome.css'

/*
import $ from 'jquery';
window.jQuery = $;
window.$ = $;
*/

Vue.use(VueResource);
Vue.http.options.root = 'http://192.168.1.26:5000/api/';

Vue.prototype.$bus = new Vue();

new Vue({
    el: '#app',
    router,
    store,
    template: '<App/>',
    components: { App }
})
  
