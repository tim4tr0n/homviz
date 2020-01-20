import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
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
  })
  