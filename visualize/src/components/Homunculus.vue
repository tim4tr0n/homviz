<template>
  <div class="homunculus">
    <div>
      <Scene @complete="complete" @before-render$="beforeRender" v-model="scene" @after-render$="++frames">
        <Camera type="arcRotate" :target="[0,1,0]" :beta="2.1" :radius="2" :alpha="Math.PI/2"></Camera>
        <HemisphericLight></HemisphericLight>
        <Asset ref="homModel" src="http://localhost:8081/guy_expanded.gltf" v-on:create-manager="handleCreateManager" v-model="homModelRoot"></Asset>
        <Cylinder :rotation="[Math.PI/2,0,0]" :position="position.twoinpp" :scaling="scale.twoinpp" v-model="twoinpp"></Cylinder>
      </Scene>
    </div>
  </div>
</template>

<script>
import * as BABYLON from 'babylonjs';
export default {
  name: 'Homunculus',
  data() {
    return {
      twoinpp: null,
      time: performance.now(),
      frames: 0,
      homModelRoot: null,
      scene: null
    };
  },
  props: {
    rotation: {
        type: Array
    },
  },
  watch: {
    homModelRoot() {
      console.log("homModelRoot CHANGED", this.homModelRoot)
    },

  },
  mounted() {
    // this.getModelDetails()
    this.loadHomunculus()
  },
  computed: {
    scale() {
      let a = this.$store.getters.sliderPosition * 0.005;

      return {
        twoinpp: [0.05, a, 0.05]
      };
    },

    // homModelRoot: {
    //   get(){
    //     console.log()
    //   }
    // }

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
    loadHomunculus() {
      console.log("loading homcunulus")
    },
    handleCreateManager(){
      console.log("morph manager created")
    },
    // getModelDetails() {
    //   console.log("homModelRoot", this.homModelRoot)

    // },
    
    onHomunculus(event) {
      console.log('onHomunculus', event);
      // the entity event includes entity reference
      this.homModelRoot = event.entity;
    },

    complete() {
      console.log('dummy', this.homModelRoot);
      console.log("scene loaded",this.scene)
      // this.homModelRoot.convertToUnIndexedMesh();

      const manager = new BABYLON.MorphTargetManager();
      const target = BABYLON.MorphTarget.FromMesh(this.homModelRoot, "homModelMorph", 1)
      console.log("hom mesh morph", target)
      manager.addTarget(target)
      this.$set(this.homModelRoot, 'morphTargetManager', manager);
      console.log("morph manager", manager)
      // cylindrical phallus
      console.log('twoinpp', this.twoinpp);
      // console.log("dummy now", this.homModelRoot)
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
