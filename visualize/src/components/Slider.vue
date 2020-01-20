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
  #slider {
    bottom: -10px;
    width: 90%;
    left: 5%;
  }
  .slidecontainer {
    width: 100%;
    /* boxShadow: '0 2pt 8pt rgba(0, 0, 0, 0.5)'' */
  }

</style>