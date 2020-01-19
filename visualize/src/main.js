import Vue from 'vue'
import App from './App.vue'
import { plugin, Scene, HemisphericLight, Camera, Asset, Cannon } from 'vue-babylonjs';
import VueFirestore from 'vue-firestore';
import { store } from './store/store'

Vue.config.productionTip = false
Vue.use(plugin, { components: { Scene, HemisphericLight, Asset, Camera, Physics: Cannon } });
Vue.use(VueFirestore);

new Vue({
  el: "#app",
  components: { App },
  store,
  template: "<App/>",
  render: h => h(App),
}).$mount('#app')
