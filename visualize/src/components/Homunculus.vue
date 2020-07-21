<template>
  <div class="Scene">
    <v-dialog/>
    <hsc-menu-style-white class="menubar">
        <hsc-menu-bar >
            <hsc-menu-bar-item label="homviz">
                <hsc-menu-separator/>
                <hsc-menu-item label="h̸͍̪̞͝ͅo̴̹̬̟̺̙̝̻̥̟͍͖̬͋̄́͊̔̾̈͛̏̈̚͘w̴͙̞̳̖̜̜̒̃̅̏" @click="openTutorialModal" />
                <hsc-menu-item label="Cease" @click="window.alert('Save')" :disabled="true" />
            </hsc-menu-bar-item>
            <hsc-menu-bar-item label="VR">
              <hsc-menu-item label="Enable" @click="openVRModal" />
            </hsc-menu-bar-item>
            <hsc-menu-bar-item label="Info">
                <hsc-menu-item label="About" @click="openAboutModal" />
            </hsc-menu-bar-item>
        </hsc-menu-bar>
    </hsc-menu-style-white>

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
  // ArcRotateCamera,
  Vector3,
  HemisphericLight,
  PointLight
} from '@babylonjs/core'

import Vue from 'vue'
import * as BABYLON from "babylonjs"
import { GLTFFileLoader } from "@babylonjs/loaders"
import * as VueMenu from '@hscmap/vue-menu'
import VModal from 'vue-js-modal'

Vue.use(VueMenu)
Vue.use(VModal, { dialog: true })

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
      bodyParts: this.$store.getters.bodyParts,
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

    window.addEventListener('mouseMoved', this.mouseMoved);

  },

  beforeDestroy() {
    this.babylon.scene.dispose()
    this.engine.dispose()
  },
  computed: {
    dbInfo() {
      return {
        bodyParts: this.$store.getters.bodyParts
      }
    }
  },
  methods: {
    openTutorialModal(){
      this.$modal.show('dialog', {
        title: 'How to',
        text: '<i>Now wouldn\'t you like to know</i>',
        buttons: [
          {
            title: 'Close'
          }
      ]
      })
    },
    openAboutModal(){
      this.$modal.show('dialog', {
        title: 'About',
        text: 'Homviz takes many books from Project Guttenberg and analyzes frequency of human anatomy, allowing a 3D visualization in the form of what we refer to as <strong>The Literary Homunculus</strong>. <br><br>Select a text from the vast Gutenberg corpus and watch with glee as different body parts scale in proportion to their number of mentions. Witness how various body parts dominate in literature across years, genres, and languages, all while being serenaded by beautiful, vintage jazz. <strong>Enjoy.</strong>',
        buttons: [
          {
            title: '<marquee>🦐🤏💧🥚</marquee>',
            handler: () => { alert('Copyright © Glowfish 2020. May our light guide legends.') }
          },
          {
            title: 'Close'
          }
      ]
      })
    },
    openVRModal(){
      this.$modal.show('dialog', {
        title: 'Enter VR Mode',
        text: 'homviz uses <u>WebVR</u> to enable VR support. Open homviz.net in a WebVR-enabled browser and connect your headset.<br><br>We recommended Firefox (not available on Chrome, unfortunately)',
        buttons: [
          {
            title: 'Get Firefox VR',
            handler: () => { window.location.href = 'https://support.mozilla.org/en-US/kb/view-virtual-reality-firefox-webvr'; }
          },
          {
            title: 'Close'
          }
      ]
      })
    },
    openLinkOne(){
      window.open("https://www.quora.com/Is-it-possible-to-create-a-homunculus-by-injecting-human-sperm-into-an-egg")
    },
    openLinkTwo(){
      window.open("https://www.youtube.com/watch?v=HNLPXzlz6-I")
    },
    updateHomunculusPart(e, meshName, targetName) {
      this.$store.commit("changeHomunculusPartByScheme", { sliderValue: e.srcElement.valueAsNumber, meshName, targetName } )
    },
    // MODIFY FOR MULTIPLE MORPH TARGETS PER MESH
    resetHomunculus(homunculusState){
        const bodyPartPaths = this.$store.getters.bodyParts
        const homunculusParts = Object.keys(homunculusState)


        for (var index = 0; index < homunculusParts.length; index++){
            const part = homunculusParts[index]
            const partPath = bodyPartPaths[part]
            if (partPath == null){
              continue
            }
            // go through every morph target for the given word that we care about
            for (var meshIndex = 0; meshIndex < partPath.meshes.length; meshIndex++){
              var mesh = partPath.meshes[meshIndex]
              for(var morphIndex = 0; morphIndex < partPath.targetNames.length; morphIndex++){
                var targetName = partPath.targetNames[morphIndex]
                // console.log("targetName", targetName)
                var thisMesh = this.morphTargetScheme[mesh]
                // console.log("thisMesh", thisMesh)
                var thisMorphTarget = thisMesh[targetName]
                thisMorphTarget.influence = 0
              }
            }
        }
    },
    // MODIFY FOR MULTIPLE MORPH TARGETS PER MESH
    async morphHomunculus(homunculusState){
        //set everything to zero, first - i realize that this is a terrible way to do it whatever
        await this.resetHomunculus(homunculusState)
        // whittle down to the parts we actually care about
        const bodyPartPaths = this.$store.getters.bodyParts
        const homunculusParts = Object.keys(homunculusState)
        const homunculusValues = Object.values(homunculusState)
        var maxValue = Math.max(...homunculusValues);
        if (maxValue == 0){
          maxValue = 1
        }
        for (var index = 0; index < homunculusParts.length; index++){
            const part = homunculusParts[index]
            const partValue = homunculusState[part]
            const partPath = bodyPartPaths[part]
            // console.log("bodyPartPaths", bodyPartPaths)
            if (partPath == null){
              continue
            }
            // go through every morph target for the given word that we care about
            for (var meshIndex = 0; meshIndex < partPath.meshes.length; meshIndex++){
              var mesh = partPath.meshes[meshIndex]
              // console.log("mesh we got within the loop", mesh)  
              for(var morphIndex = 0; morphIndex < partPath.targetNames.length; morphIndex++){
                var targetName = partPath.targetNames[morphIndex]
                // console.log("targetName", targetName)
                var thisMesh = this.morphTargetScheme[mesh]
                // console.log("thisMesh", thisMesh)
                var thisMorphTarget = thisMesh[targetName]
                var currentMorphInfluence = thisMorphTarget.influence
                var newInfluence = partValue / maxValue
                if (currentMorphInfluence < newInfluence){
                  thisMorphTarget.influence = newInfluence // change the way we do maximum here
                }
              }
            }
        }
    },
    changeMorphTarget(e, index){
        this.morphTargets[index].influence = e.srcElement.valueAsNumber / 100
    },
    async importHom(scene) {
      var homModel = null
      BABYLON.SceneLoader.RegisterPlugin(new GLTFFileLoader())
      var sceneLoader = BABYLON.SceneLoader.Append("/", "homunculus_final_product.gltf", scene, async (meshes) => {
            // Create a default arc rotate camera and light.
         
            scene.createDefaultCameraOrLight(true, true, true);
            scene.createDefaultEnvironment();
            scene.activeCamera.useAutoRotationBehavior = true;
            scene.activeCamera.lowerRadiusLimit = 1;
            scene.activeCamera.upperRadiusLimit = 2.5;
            

 
            // The default camera looks at the back of the asset.
            // Rotate the camera by 180 degrees to the front of the asset.
            // scene.activeCamera.position = new BABYLON.Vector3(1,1,5)
            scene.activeCamera.alpha += Math.PI;
            // scene.activeCamera.beta += Math.PI;
            console.log("all meshes available", meshes)

            // var meshes = []
            homModel = meshes.meshes[2] // TODO: grab this programmatically (at least for production)
            console.log("homModel that we brought in!", homModel)

            console.log("morphTargetManager", homModel.morphTargetManager)

            var morphTargets = []
            for ( var managerIndex = 0; managerIndex < meshes.morphTargetManagers.length; managerIndex++){
              var morphTargetManager = meshes.morphTargetManagers[managerIndex]
              for ( var index = 0; index < morphTargetManager.numTargets; index++ ) {
                var morphTarget = homModel.morphTargetManager.getTarget(index)  
                morphTargets.push(morphTarget)
              }
            }
            
            console.log("total morphTargets")
            console.log(morphTargets)
            // this is extremely dangerous. no guarantee that it loads in time. pls add promise or something
            console.log("manifest scheme output within THIS", this.manifestScheme)

            // populate morph target scheme
            var morphTargetScheme = {}
            for ( var meshIndex = 2; meshIndex < meshes.meshes.length; meshIndex++){
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
                // console.log(meshName, "=>", manifestSubObject)
                var targetNamesArray = Object.keys(manifestSubObject)
                var subObject = morphTargetScheme[meshName]
                var morphTargetName =  targetNamesArray[morphTargetIndex]

                subObject[morphTargetName] = thisMorphTarget
              }
            }

            console.log("morphTargetScheme Output", morphTargetScheme)
            this.morphTargetScheme = morphTargetScheme
            this.morphTargets = morphTargets

      });
      sceneLoader.onParsedObservable.add(gltfBabylon => {
        var manifest = gltfBabylon.json;
        // console.log("MANIFEST", manifest)
        // go through GLTF file to get morphTarget names (this is really fuckin stupid, shame on babylon for not building morph names into their parser)
        var manifestScheme = {}

        for ( var meshIndex = 0; meshIndex < manifest.meshes.length; meshIndex++){
          var mesh = manifest.meshes[meshIndex]
          var meshName = mesh.name
          manifestScheme[meshName] = {}

          var meshObject = manifestScheme[meshName]
          if(mesh.extras == null){
            // console.log("SKIPPING THAT SHIT")
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

      // var camera = new BABYLON.ArcRotateCamera(
      //   'Camera',
      //   Math.PI / 2,
      //   Math.PI / 2,
      //   2,
      //   Vector3.Zero(),
      //   this.babylon.scene
      // )
      
      
      
      // VR CHANGES
      var camera = new BABYLON.WebVRFreeCamera(
        "Camera",
        new BABYLON.Vector3(
          5,
          Math.PI,
          7,
        ),
        this.babylon.scene
      );

      camera.attachControl(this.$refs.canvas, true)

      // scene.onPointerDown = function() {
      //     scene.onPointerDown = undefined;
      //     camera.attachControl(this.$refs.canvas, true);
      // };

      var vrHelper = scene.createDefaultVRExperience();

      vrHelper.displayGaze = true ;
      vrHelper.displayLaserPointer = true;
      vrHelper.changeGazeColor(new BABYLON.Color3(1,1,1));
      vrHelper.enableInteractions();

      // Code for edge/Safari VR 
      vrHelper.onEnteringVR.add(()=> {
          scene.getEngine().isPointerLock = true;
      })

      vrHelper.onExitingVR.add( ()=> {
          scene.getEngine().isPointerLock = false;
      })
      
      //-----------------------------------------------

      // var skybox = BABYLON.Mesh.CreateBox("skyBox", 100.0, scene);
      // var skyboxMaterial = new BABYLON.StandardMaterial("skyBox", scene);
      // skyboxMaterial.backFaceCulling = false;
      // skyboxMaterial.reflectionTexture = new BABYLON.CubeTexture("background", scene);
      // skyboxMaterial.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE;
      // skyboxMaterial.diffuseColor = new BABYLON.Color3(0, 0, 0);
      // skyboxMaterial.specularColor = new BABYLON.Color3(0, 0, 0);
      // skyboxMaterial.disableLighting = true;
      // skybox.material = skyboxMaterial;

      // new HemisphericLight('light1', new Vector3(1, 1, 0), this.babylon.scene)
      // new HemisphericLight('light4', new Vector3(-2, -4, 0), this.babylon.scene)
      new HemisphericLight('light5', new Vector3(-2, 4, 0), this.babylon.scene)
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
hsc-menu-bar-item {
  font-size: 13px
}
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

.menubar {
  position: absolute;
  border-radius: 0 0 4pt 0;
}
</style>
