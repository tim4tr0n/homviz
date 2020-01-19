<template>
  <div class="homunculus">
    <div>
      <!-- events take either a method name or logic content-->
      <!-- the complete event happens after all children have been initialized and bound-->
      <Scene @complete="complete" @before-render$="beforeRender" @after-render$="++frames">
        <!-- you can use v-model bindings instead of event entity reference-->
        <Camera type="arcRotate" :target="[0,1,0]" :radius="5" :alpha="Math.PI/4"></Camera>
        <HemisphericLight></HemisphericLight>
        <Asset src="https://srv-file4.gofile.io/download/Tryf1D/dummy3.babylon"></Asset>
        <Cylinder :rotation="[Math.PI/2,0,0]" :position="position.twoinpp" :scaling="scale.twoinpp" v-model="twoinpp"></Cylinder>
      </Scene>
      <div v-text="`Frames: ${frames}`" style="position: absolute; color: white; bottom: 0; padding: 15px"></div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Homunculus',
  data() {
    return {
      twoinpp: null,
      time: performance.now(),
      frames: 0,
    };
  },

  // TODO : fix props validation error in console god dammit

  props: {
    rotation: {
        type: Array
    },
  },

  computed: {
    scale() {
      let a = this.$store.getters.sliderPosition * 0.005;

      return {
        twoinpp: [0.05, a, 0.05]
      };
    },

    position() {
      let b = (this.$store.getters.sliderPosition * 0.005);

      return {
        twoinpp: [0,0.9,b]
      }
    }

    // rotate() {
    //   let y = this.$store.getters.sliderPosition;

    //   return {
    //     dummy: [0, y, 0]
    //   }
    // }
  },

  methods: {
    beforeRender() {
      this.time = performance.now();
    },

    onDummy(event) {
      console.log('onDummy', event);
      // the entity event includes entity reference
      this.dummy = event.entity;
    },

    complete() {
      console.log('dummy', this.dummy);
      console.log('twoinpp', this.twoinpp);
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
