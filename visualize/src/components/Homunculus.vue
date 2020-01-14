<template>
  <div class="hello">
    <div>
      <!-- events take either a method name or logic content-->
      <!-- the complete event happens after all children have been initialized and bound-->
      <Scene @complete="complete" @before-render$="beforeRender" @after-render$="++frames">
        <!-- you can use v-model bindings instead of event entity reference-->
        <Box :position="[-2, 0, 5]" :scaling="scale.box" v-model="box"></Box>
        <Sphere :position="[2, 0, 5]" :scaling="scale.sphere" @entity="onSphere"></Sphere>
      </Scene>
      <div v-text="`Frames: ${frames}`" style="position: absolute; color: white; bottom: 0; padding: 15px"></div>
    </div>
      <Slide id="slide"/>
  </div>
</template>

<script>

import Slide from './Slider.vue';
// var sliderval = document.getElementById("slide");
// var output = sliderval.value;
// sliderval.oninput = function() {
//   output = this.value;
// }

export default {
  name: 'Homunculus',
  components: {
    Slide
  },
  props: {
    msg: String
  },
  data() {
    return {
      box: null,
      sphere: null,
      time: performance.now(),
      frames: 0,
    };
  },

  computed: {
    scale() {
      let a = 2 + Math.cos(this.time * 0.001);
      let b = 2 + Math.sin(this.time * 0.001);
      return {
        box: [a, b, 1],
        sphere: [b, a, 1],
      };
    },
  },

  methods: {
    beforeRender() {
      this.time = performance.now();
    },

    onSphere(event) {
      console.log('onSphere', event);
      // the entity event includes entity reference
      this.sphere = event.entity;
    },

    complete(event) {
      console.log('complete', event);
      console.log('box', this.box);
      console.log('sphere', this.sphere);
    },
  },
};
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
