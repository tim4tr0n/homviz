<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      For a guide and recipes on how to configure / customize this project,<br>
      check out the
      <a href="https://cli.vuejs.org" target="_blank" rel="noopener">vue-cli documentation</a>.
    </p>
    <h3>Installed CLI Plugins</h3>
    <!-- <nouislider></nouislider> -->
    <vue-form-generator @model-updated="changeSlider" :schema="schema" :model="model" :options="formOptions"></vue-form-generator>
    <h3>hOLY FUCKE AOUHAEHOUHEFA</h3>
    {{ model }}

    <div @input="changeSlider" id="slider" ref="slider"></div>
   
  </div>
</template>

<script>
import Vue from 'vue'
import VueFormGenerator from 'vue-form-generator'
import 'vue-form-generator/dist/vfg.css'
import noUiSlider from 'nouislider';

Vue.use(VueFormGenerator)

export default {
  name: 'TestSlider',
  props: {
    msg: String
  },
  methods: {
    changeSlider: function(event){
      console.log(event)
    },
    updateSlider: function updateSlider() {
      console.log("updated")
      this.$refs.slider.noUiSlider.set([this.minRange, this.maxRange]);
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
            return value + 'AD';
          },
          from: function ( value ) {
            return value.replace('AD', '');
          }
        }
      }
    }); 
            
    this.Slider.noUiSlider.on('update',(values, handle) => {
      console.log(values)
      this[handle ? 'maxRange' : 'minRange'] = parseInt(values[handle]);
    }); 
  },
  data () {
    return {
      slider: {
        startMin: 25,
        startMax: 75,
        min: 0,
        max: 100,
        start: 40,
        step: 1
      },
      Slider: document.getElementById('slider'),
      model: {
        id: 1,
        name: 'John Doe',
        password: 'J0hnD03!x4',
        skills: ['Javascript', 'VueJS'],
        email: 'john.doe@gmail.com',
        status: true,
      },
      schema: {
        fields: [          
          {
            type: "noUiSlider",
            label: "Volume level",
            model: "volume",
            min: 0,
            max: 140,
            required: true,
            noUiSliderOptions: {
                connect: "lower",
                range:{
                  'min': [0],
                  '10%': [10, 10],
                  '50%': [80, 50],
                  '80%': 150,
                  'max': 200
                },
                tooltips: [true],
                // step: 10,
                pips: {
                  mode: 'steps',
                  density: 5,
                  filter: function( value ) {return value % 4 ? 2 : 1;},
                  format: {
                    to: function ( value ) {
                      return value + 'dB';
                    },
                    from: function ( value ) {
                      return value.replace('dB', '');
                    }
                  }
                }
            },
            validator: VueFormGenerator.validators.required
          },
          {
            type: "noUiSlider",
            label: "Volume level",
            model: "volume",
            min: 0,
            max: 100,
            required: true,
            noUiSliderOptions: {
              connect: "lower",
            },
            validator: VueFormGenerator.validators.required
          }
        ]
      },
      formOptions: {
        validateAfterLoad: true,
        validateAfterChanged: true,
        validateAsync: true
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
