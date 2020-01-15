import Vue from 'vue'
import App from './App.vue'
import { plugin, Scene, Box, Cannon } from 'vue-babylonjs';
import VueFirestore from 'vue-firestore';

Vue.config.productionTip = false
Vue.use(plugin, { components: { Scene, Box, Physics: Cannon } });
Vue.use(VueFirestore);

new Vue({
  render: h => h(App),
}).$mount('#app')
