import Vue from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'
import VueRouter from "vue-router";
import {routes} from "./routes.js";
import store from "./store/store";
import axios from "axios";
import {baseurl} from "@/urls";
import VueFilterDateFormat from 'vue-filter-date-format';
import VueCookies from 'vue-cookies'
import * as Sentry from '@sentry/browser';
import {Vue as VueIntegration} from '@sentry/integrations';

const moment = require('moment');

Sentry.init({
    dsn: 'https://17e6fa53841f49ec9bb9f2de72cbcba3@o385268.ingest.sentry.io/5217730',
    integrations: [new VueIntegration({Vue, attachProps: true})],
});
Vue.use(VueRouter);
// Install BootstrapVue
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);
//for filters of Date & it's formatting
Vue.use(VueFilterDateFormat);
// for cookies
Vue.use(VueCookies);

Vue.filter('dateformatter', function (date) {
    return moment(date).format("DD-MM-YYYY");
});


const router = new VueRouter({
    routes,
    mode: "history"
});

axios.defaults.baseURL = baseurl;
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

axios.interceptors.request.use(req => {
    if (store.state.loggedIn) {
        req.headers['Authorization'] = "Bearer " + store.state.userdata.token;
    }
    return req;
});


Vue.config.productionTip = false;

new Vue({
    router,
    store,
    render: h => h(App),
}).$mount('#app');
