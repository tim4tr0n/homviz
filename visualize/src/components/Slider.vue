<template>
<div class="slidecontainer">
  <input type="range" min="1" max="100" value="1" class="slider" id="slide">
</div>
</template>

<script>
export default{
    name: 'Slide',
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.slidecontainer {
  width: 100%;
}

.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 25px;
  background: #d3d3d3;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

.slider:hover {
  opacity: 1;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 25px;
  background: #9400D3;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 25px;
  height: 25px;
  background: #9400D3;
  cursor: pointer;
}
</style>