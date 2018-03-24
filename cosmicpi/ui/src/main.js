import Vue from 'vue';
import VueResource from 'vue-resource';
import { Settings } from 'luxon'
import router from './router.js'
import store from './store.js';
import App from './App.vue';
import './assets/css/main.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'font-awesome/css/font-awesome.css';
import 'vue-datetime/dist/vue-datetime.css';


Vue.use(VueResource);
Vue.http.options.root = API_URL;
Settings.defaultLocale = 'en'


new Vue({
    el: '#app',
    router,
    store,
    template: '<App/>',
    components: { App },
})
  
