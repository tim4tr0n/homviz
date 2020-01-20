<template>
  <div class="slidecontainer">
    <div id="slider" ref="slider"></div>
  </div>
</template>



<script>
import noUiSlider from 'nouislider';
export default {
  data () {
    return {
      sliderValue: null,
      slider: {
          startMin: 25,
          startMax: 75,
          min: 0,
          max: 100,
          start: 40,
          step: 1
      },
      Slider: document.getElementById('slider'),
    }
  },
  mounted: function() {
    this.Slider = document.getElementById('slider')
    noUiSlider.create(this.Slider, {
      start: [this.slider.startMin],
      step: this.slider.step,
      tooltips: [true],
      range:{
        'min': [0],
        '10%': [10, 10],
        '50%': [80, 50],
        '80%': 150,
        'max': 200
      },
      pips: {
        mode: 'steps',
        density: 5,
        filter: function( value ) {return value % 4 ? 2 : 1;},
        format: {
          to: function ( value ) {
            return value + ' ';
          },
          from: function ( value ) {
            return value.replace(' ', '');
          }
        }
      }
    }); 
            
    this.Slider.noUiSlider.on('update',(values) => {
      this.$store.commit('changeSlider', values[0])
    }); 
  }
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