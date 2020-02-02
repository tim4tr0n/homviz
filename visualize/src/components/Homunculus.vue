<template>
  <div class="Scene">
    <canvas
      id="renderCanvas"
      ref="canvas"
      class="Scene-canvas"
      touch-action="none"
      oncontextmenu="return false"
    ></canvas>

    <div v-if="this.debug == true">
      <div v-for="meshName in Object.keys(morphTargetScheme)" v-bind:key="meshName.idx">
        <h4>{{meshName}}</h4>
        <div v-for="targetName in Object.keys(morphTargetScheme[meshName])"  v-bind:key="targetName.idx">
          <input type="range" @input="($event) => { updateHomunculusPart( $event, meshName, targetName ) }"/>{{targetName}}
        </div>
      </div>
    </div>

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
// import HomunculusModel from "../../public/homunculus_fin.gltf"

export default {
  name: 'Homunculus',

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
      morphTargets: [],
      morphTargetScheme: {},
      manifestScheme: {},
      debug: false
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
        this.morphTargets[1].influence = mutation.payload.sliderValue / 100
      }

      if(mutation.type == "changeHomunculusPartByIndex"){
        this.morphTargets[mutation.payload.index].influence = mutation.payload.sliderValue / 100
      }

      if(mutation.type == "changeHomunculusPartByScheme"){
        var subObject = this.morphTargetScheme[mutation.payload.meshName]
        var morphTarget = subObject[mutation.payload.targetName]
        morphTarget.influence = mutation.payload.sliderValue / 100
      }
    });

    //need to port this to a function and do a lot more complex stuff to make this actually look good
    this.$store.subscribe((mutation) => {
      if( mutation.type == "changeHomunculusState"){
        console.log("CHANGE HOMUNCULUS STATE")
        const homunculusState = mutation.payload
        this.morphHomunculus(homunculusState)
      }
    });
  },

  beforeDestroy() {
    this.babylon.scene.dispose()
    this.engine.dispose()
  },
  methods: {
    updateHomunculusPart(e, meshName, targetName) {
      this.$store.commit("changeHomunculusPartByScheme", { sliderValue: e.srcElement.valueAsNumber, meshName, targetName } )
    },
    // MODIFY FOR MULTIPLE MORPH TARGETS PER MESH
    morphHomunculus(homunculusState){
        const homunculusParts = Object.keys(homunculusState)
        const homunculusValues = Object.values(homunculusState)
        const maxValue = Math.max(...homunculusValues);
        for (var index = 0; index < homunculusParts.length; index++){
            const partValue = homunculusState[homunculusParts[index]]
            this.morphTargets[index].influence = partValue / maxValue
        }
    },
    changeMorphTarget(e, index){
        this.morphTargets[index].influence = e.srcElement.valueAsNumber / 100
    },
    async importHom(scene) {
      var homModel = null
      BABYLON.SceneLoader.RegisterPlugin(new GLTFFileLoader())
      var self = this
      console.log("THIS", this)
      var sceneLoader = BABYLON.SceneLoader.Append("/", "homunculus_fin.gltf", scene, async (meshes) => {
            // Create a default arc rotate camera and light.
            scene.createDefaultCameraOrLight(true, true, true);
            scene.createDefaultEnvironment();
            scene.activeCamera.useAutoRotationBehavior = true;
            scene.activeCamera.lowerRadiusLimit = 1;
            scene.activeCamera.upperRadiusLimit = 15;
            
            // The default camera looks at the back of the asset.
            // Rotate the camera by 180 degrees to the front of the asset.
            scene.activeCamera.position = new BABYLON.Vector3(1,1,5)
            scene.activeCamera.alpha += Math.PI;
            // scene.activeCamera.beta += Math.PI;
            console.log("all meshes available", meshes)

            // var meshes = []
            homModel = meshes.meshes[1] // TODO: grab this programmatically (at least for production)
            console.log("homModel that we brought in!", homModel)

            console.log("morphTargetManager", homModel.morphTargetManager)

            console.log("for loop morph  manager",  meshes.morphTargetManagers.length)

            var morphTargets = []
            for ( var managerIndex = 0; managerIndex < meshes.morphTargetManagers.length; managerIndex++){
              var morphTargetManager = meshes.morphTargetManagers[managerIndex]
              for ( var index = 0; index < morphTargetManager.numTargets; index++ ) {
                var morphTarget = homModel.morphTargetManager.getTarget(index)  
                morphTargets.push(morphTarget)
              }
            }
            

            // this is extremely dangerous. no guarantee that it loads in time. pls add promise or something
            console.log("manifest scheme output within THIS", this.manifestScheme)

            // populate morph target scheme
            var morphTargetScheme = {}
            for ( var meshIndex = 1; meshIndex < meshes.meshes.length; meshIndex++){
              var mesh = meshes.meshes[meshIndex]
              // console.log("mesh in loop:", mesh)
              var meshName = mesh.name
              morphTargetScheme[meshName] = {}
              //now populate with morph targets
              if ( mesh.morphTargetManager == null){
                continue
              }
              for ( var morphTargetIndex = 0; morphTargetIndex < mesh.morphTargetManager.numTargets; morphTargetIndex++){

                var thisMorphTarget = mesh.morphTargetManager.getTarget(morphTargetIndex)
                // console.log("morph target within for loop:", thisMorphTarget)
                // console.log("morph target scheme so far", morphTargetScheme)

                var manifestSubObject = this.manifestScheme[meshName]
                console.log(meshName, "=>", manifestSubObject)
                var targetNamesArray = Object.keys(manifestSubObject)
                var subObject = morphTargetScheme[meshName]
                var morphTargetName =  targetNamesArray[morphTargetIndex]

                subObject[morphTargetName] = thisMorphTarget
              }
            }

            console.log("morphTargetScheme Output", morphTargetScheme)
            console.log("morphTargets", morphTargets)
            console.log("SELF", self)
            console.log("THIS", this)
            this.morphTargetScheme = morphTargetScheme
            this.morphTargets = morphTargets

      });
      sceneLoader.onParsedObservable.add(gltfBabylon => {
        var manifest = gltfBabylon.json;
        console.log("MANIFEST", manifest)
        // go through GLTF file to get morphTarget names (this is really fuckin stupid, shame on babylon for not building morph names into their parser)
        var manifestScheme = {}

        for ( var meshIndex = 0; meshIndex < manifest.meshes.length; meshIndex++){
          var mesh = manifest.meshes[meshIndex]
          var meshName = mesh.name
          manifestScheme[meshName] = {}

          var meshObject = manifestScheme[meshName]
          if(mesh.extras == null){
            console.log("SKIPPING THAT SHIT")
            continue
          }
          for ( var morphNameIndex = 0; morphNameIndex < mesh.extras.targetNames.length; morphNameIndex++){
            var targetName = mesh.extras.targetNames[morphNameIndex]
            meshObject[targetName] = null
          }
        }
        this.manifestScheme = manifestScheme
      })
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
