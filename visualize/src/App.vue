<template>
  <div id="app">
    
    <Slide id="slide"/>
    <Selectors id="selectors"/>
    <Stats id="stats"/>
    <Homunculus id="homunculus"/>
  </div>
</template>

<script>
  import Homunculus from './components/Homunculus.vue';
  import Slide from './components/Slider.vue';
  import Stats from './components/Stats.vue';
  import Selectors from './components/Selectors.vue';

  export default {
    name: 'app',
    components: {
      Homunculus,
      Slide,
      Stats,
      Selectors
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
    margin-top: -8px;
    position: relative
  }
  #slide {
    position: absolute;
    bottom: 0px;
    height: 10%;
    background: linear-gradient( rgba(0, 0, 0, 0.25) 100%, #436f7c 100%),
  url('/static/bg.jpg') no-repeat center center fixed;
    z-index: 4;
  }
  #homunculus {
    width: 100%;
    position: relative;
  }
  #selectors {
    z-index: 4;
    position: absolute
  }
  #stats {
    z-index: 3;
    right: 0%;
    position: absolute
  }
</style>
