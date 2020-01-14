<template>
  <div id="app">
    <Homunculus msg="Welcome to Your Vue.js App" id="homunculus"/>
  </div>
</template>

<script>
import Homunculus from './components/Homunculus.vue';

export default {
  name: 'app',
  components: {
    Homunculus
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
  vertical-align: top;
}
</style>
