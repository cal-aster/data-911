import Vue from 'vue';
import axios from 'axios';
import App from './App.vue';
import store from './store';
import router from './router';
import vuetify from './plugins/vuetify';
import VueGtag from 'vue-gtag';

Vue.use(
  VueGtag,
  {
    config: { id: 'G-ZZDN92GEE8' },
    enabled: process.env.NODE_ENV === 'production',
  },
  router,
);

Vue.prototype.$http = axios;
Vue.config.productionTip = false;

axios.defaults.baseURL = process.env.VUE_APP_BASE_URL;
axios.defaults.headers.common.Accept = 'application/json';

new Vue({
  store,
  router,
  vuetify,
  components: { app: App },
  render: (h) => h(App),
}).$mount('#app');
