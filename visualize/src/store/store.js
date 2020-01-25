import Vue from 'vue'
import Vuex from 'vuex'
import VuexEasyFirestore from 'vuex-easy-firestore'

import { initFirebase, firebase } from '../firebaseConfig';

Vue.use(Vuex)

const booksModule = {
  firestorePath: 'books',
  firestoreRefType: 'collection', // or 'doc'
  moduleName: 'booksModule',
  statePropName: 'data',
  namespaced: true, // automatically added

  // this object is your store module (will be added as '/myModule')
  // you can also add state/getters/mutations/actions
  state: {
    topBooks: []
  },
  getters: {},
  mutations: {},
  actions: {},
}

initFirebase()
  .then( console.log("Firebase initialized!") )
  .catch( err => console.error(err))

const easyFirestore = VuexEasyFirestore(
  [booksModule],
  {logging: true, FirebaseDependency: firebase}
)
  
const storeData = {
  plugins: [easyFirestore],
  state: {
    bodyState: 3,
    sliderPosition: 0,
  },
  mutations: {
    changeSlider(state, value) {
      state.sliderPosition = value
    },
    changeBodyState(state, value) {
      state.bodyState = value
    }
  },
  getters: {
    bodyState: state => state.bodyState,
    sliderPosition: state => state.sliderPosition
  },
  strict: process.env.NODE_ENV !== 'production'
}

export const store = new Vuex.Store(storeData);
  