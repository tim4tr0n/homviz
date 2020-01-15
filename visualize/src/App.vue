<template>
  <div id="app">
    <Homunculus id="homunculus"/>
    <Stats id="stats"/>
    <Slide id="slide"/>
  </div>
</template>

<script>
  import Homunculus from './components/Homunculus.vue';
  import Slide from './components/Slider.vue';
  import Stats from './components/Stats.vue';
  import { db } from './firebaseConfig';

  export default {
    name: 'app',
    data() {
      return {
        books: []
      }
    },
    firestore() {
      return {
        books: db.collection('books'),
      }
    },
    components: {
      Homunculus,
      Slide,
      Stats
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 2px;
  }
  #homunculus {
    height: 90%;
    vertical-align: "absolute";
    z-index: -1;
  }
  #stats {
    position: "relative";
    bottom: 0;
    left: 0;
  }
</style>
