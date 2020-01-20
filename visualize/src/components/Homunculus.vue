<template>
  <div class="homunculus">
    <div>
      <Scene @complete="complete" @before-render$="beforeRender" @after-render$="++frames">
        <Box :position="[-2, 0, 5]" :rotation="rotate.box" :scaling="scale.box" v-model="box"></Box>
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
      box: null,
      sphere: null,
      time: performance.now(),
      frames: 0,
    };
  },
  props: {
    rotation: {
        type: Array
    },
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
    rotate() {
      let y = parseFloat(this.$store.getters.sliderPosition);
      return {
        box: [0, y, 1]
      }
    }
  },

  methods: {
    beforeRender() {
      this.time = performance.now();
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
