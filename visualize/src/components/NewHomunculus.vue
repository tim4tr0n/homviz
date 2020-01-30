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
  PointLight,
  Mesh
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

      sphere: {
        visible: true,
        position: {
          x: 0,
          y: 0,
          z: 0
        }
      }
    }
  },

  mounted() {
    this.createScene()

    this.babylon.sceneReady = true
    this.babylon.canvas = this.$refs.canvas


  },

  beforeDestroy() {
    this.babylon.scene.dispose()
    this.engine.dispose()
  },

  methods: {
    importHom(scene){
      var homModel = null
      BABYLON.SceneLoader.RegisterPlugin(new GLTFFileLoader())
      BABYLON.SceneLoader.Append("/", "guy_expanded.gltf", scene, async function (meshes) {
            // Create a default arc rotate camera and light.
          scene.createDefaultCameraOrLight(true, true, true);
          console.log("meshers", meshes.meshes)
          scene.activeCamera.useAutoRotationBehavior = true;
          scene.activeCamera.lowerRadiusLimit = 1;
          scene.activeCamera.upperRadiusLimit = 4;
            // The default camera looks at the back of the asset.
            // Rotate the camera by 180 degrees to the front of the asset.
          scene.activeCamera.alpha += 2*Math.PI;
          // console.log("READY TO RETURN homModel!")
          homModel = meshes.meshes[2]
          console.log("homModel that we brought in!", homModel)

          console.log("morphTargetManager", homModel.morphTargetManager)

          const target0 = homModel.morphTargetManager.getTarget(13)
          console.log("target #0", target0)

          target0.influence = 1

      });
      // console.log("READY TO RETURN homModel!")
      // console.log( await homModel)
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

      // LOADING IN MY FUCKING GLTF OH GOD
      this.importHom(scene)


      var newSphere = Mesh.CreateSphere(
        "sphere",
        16,
        0.5,
        this.babylon.scene
      )
      newSphere.position = new BABYLON.Vector3(0,0, 0);

      var camera = new ArcRotateCamera(
        'Camera',
        Math.PI / 2,
        Math.PI / 2,
        2,
        Vector3.Zero(),
        this.babylon.scene
      )
      camera.attachControl(this.$refs.canvas, true)

      // MORPH TARGET SHIT
      var material0 = new BABYLON.StandardMaterial("mat0", this.babylon.scene);
      material0.diffuseColor = new BABYLON.Color3(1, 0, 0);
      
      var material1 = new BABYLON.StandardMaterial("mat1", this.babylon.scene);
      material1.diffuseColor = new BABYLON.Color3(0, 0, 1);
      
      var material2 = new BABYLON.StandardMaterial("mat2", this.babylon.scene);
      material2.emissiveColor = new BABYLON.Color3(0.4, 0, 0.4);

      var multimat = new BABYLON.MultiMaterial("multi", this.babylon.scene);
      multimat.subMaterials.push(material0);
      multimat.subMaterials.push(material1);
      multimat.subMaterials.push(material2);
      newSphere.material = multimat

      var spherePositions=newSphere.getVerticesData(BABYLON.VertexBuffer.PositionKind);
      console.log('spherePositions',spherePositions.slice(0,200));

      var manager = new BABYLON.MorphTargetManager();
      newSphere.morphTargetManager = manager;

      var t0Pos = spherePositions.map((spherePos, idx)=>{
          if (idx%2 === 0 && idx < spherePositions.length/2) {
              console.log("hitting this block!")
              return spherePos*0.1;
          } else {
          return spherePos*1;
          }
      });
      
      var target0 = BABYLON.MorphTarget.FromMesh(newSphere, "sphereMorph", 0.5);
      var target1 = BABYLON.MorphTarget.FromMesh(newSphere, "secondarySphere", 0.5);
      var target2 = BABYLON.MorphTarget.FromMesh(newSphere, "secondarySphere", 0.5);
      manager.addTarget(target0);
      manager.addTarget(target1);
      manager.addTarget(target2);
      target0.setPositions(t0Pos);


      console.log(newSphere)
      console.log("manager", manager)
      var angle = 0;
      this.babylon.scene.registerBeforeRender(function() {
          console.log("running!")
          target0.influence = Math.sin(angle)*Math.sin(angle);
          angle += 0.01;
      })

      new HemisphericLight('light1', new Vector3(1, 1, 0), this.babylon.scene)
      new PointLight('light2', new Vector3(0, 1, -1), this.babylon.scene)
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
