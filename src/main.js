import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from "@/store";
// 引入element-ui
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import './assets/global.css'
Vue.config.productionTip = false
Vue.use(ElementUI);

new Vue({
  router,
  render: h => h(App),
  store
}).$mount('#app')
