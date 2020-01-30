<template>
  <div class="Scene">
    <canvas
      id="renderCanvas"
      ref="canvas"
      class="Scene-canvas"
      touch-action="none"
      oncontextmenu="return false"
    ></canvas>
  </div>
</template>

<script>
import {
  Engine,
  Scene,
  ArcRotateCamera,
  Vector3,
  HemisphericLight,
  PointLight
} from '@babylonjs/core'

import * as BABYLON from "babylonjs"
import { GLTFFileLoader } from "@babylonjs/loaders"


export default {
  name: 'NewHomunculus',

  provide() {
    return {
      babylon: this.babylon
    }
  },

  data() {
    return {
      babylon: {
        scene: undefined,
        sceneReady: false,
        canvas: undefined
      },
      morphTargets: []
    }
  },

  mounted() {
    this.createScene()

    this.babylon.sceneReady = true
    this.babylon.canvas = this.$refs.canvas


    //RESPOND TO BODY STATE CHANGE AND MODIFY HOMUNCULUS IN KIND
    //this is a pretty sketchy way to respond to state change for modifying our custom morph values. a bit unclean. meditate on this.
    this.$store.subscribe((mutation) => {
      if( mutation.type == "changeHomunculusPartState"){
        this.morphTargets[9].influence = mutation.payload.sliderValue / 100
      }
    });

    //need to port this to a function and do a lot more complex stuff to make this actually look good
    this.$store.subscribe((mutation) => {
      if( mutation.type == "changeHomunculusState"){
        console.log("CHANGE HOMUNCULUS STATE")
        const homunculusState = mutation.payload
        const homunculusParts = Object.keys(homunculusState)
        const homunculusValues = Object.values(homunculusState)
        const maxValue = Math.max(...homunculusValues);
        for (var index = 0; index < homunculusParts.length; index++){
            const partValue = homunculusState[homunculusParts[index]]
            console.log("homunculusPart", homunculusParts[index])
            console.log("value to set", partValue, maxValue)
            this.morphTargets[index].influence = partValue / maxValue
        }
      }
    });

  },

  beforeDestroy() {
    this.babylon.scene.dispose()
    this.engine.dispose()
  },

  methods: {
    
    changeMorphTarget(e, index){
        this.morphTargets[index].influence = e.srcElement.valueAsNumber / 100
    },
    importHom(scene) {
      var homModel = null
      BABYLON.SceneLoader.RegisterPlugin(new GLTFFileLoader())
      var self = this
      console.log("THIS", this)
      BABYLON.SceneLoader.Append("/", "guy_expanded.gltf", scene, async (meshes) => {
            // Create a default arc rotate camera and light.
            scene.createDefaultCameraOrLight(true, true, true);
            scene.activeCamera.useAutoRotationBehavior = true;
            scene.activeCamera.lowerRadiusLimit = 1;
            scene.activeCamera.upperRadiusLimit = 2.5;

            // The default camera looks at the back of the asset.
            // Rotate the camera by 180 degrees to the front of the asset.
            scene.activeCamera.alpha += Math.PI;

            homModel = meshes.meshes[1] // TODO: grab this programmatically (at least for production)
            console.log("homModel that we brought in!", homModel)

            console.log("morphTargetManager", homModel.morphTargetManager)


            var morphTargets = []
            for ( var index = 0; index < homModel.morphTargetManager.numTargets; index++ ) {
                var morphTarget = homModel.morphTargetManager.getTarget(index)  
                morphTargets.push(morphTarget)
            }
            console.log("morphTargets", morphTargets)
            console.log("SELF", self)
            console.log("THIS", this)
            this.morphTargets = morphTargets

      });
    },
    createScene() {
      // Create render loop, a camera and some basic lights:
      this.engine = new Engine(
        this.$refs.canvas,
        true,
        { preserveDrawingBuffer: true },
        false
      )

      var scene = this.babylon.scene = new Scene(this.engine)

      this.importHom(scene)

      var camera = new ArcRotateCamera(
        'Camera',
        Math.PI / 2,
        Math.PI / 2,
        2,
        Vector3.Zero(),
        this.babylon.scene
      )
      camera.attachControl(this.$refs.canvas, true)

      new HemisphericLight('light1', new Vector3(1, 1, 0), this.babylon.scene)
      new HemisphericLight('light4', new Vector3(-2, -4, 0), this.babylon.scene)
      new PointLight('light2', new Vector3(0, 1, -1), this.babylon.scene)
      new PointLight('light3', new Vector3(1, 1, 1), this.babylon.scene)
      // this.babylon.scene.debugLayer.show();
      this.engine.runRenderLoop(() => {
        this.babylon.scene.render()
      })
    },

    layout() {
      if (this.engine) this.engine.resize()
    }
  }
}
</script>

<style lang="scss">
.Scene {
  position: relative;
  width: 100%;
  height: 100%;
}

.Scene-canvas {
  width: 100%;
  height: 100%;
  touch-action: none;
  outline: none;
  display: block;
}
</style>
