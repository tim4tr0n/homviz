<template>
  <div id="container"></div>
</template>
<script>
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
// import * as dat from 'dat.gui';
// import { Character } from "./../3d/Character"
// import testconfig from "./../../public/models/skinned/testconfig.json"
// import axios from 'axios';
export default {
  name: 'NewHomunculus',
  data() {
    return {
      cube: null,
      renderer: null,
      scene: null,
      camera: null
    }
  },
  methods: {
    init: function() {
        THREE.Cache.enabled = false;
        this.scene = new THREE.Scene()
        this.scene.background = new THREE.Color( 0x38374c );
        this.camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            2000
        )
        
        this.renderer = new THREE.WebGLRenderer()
        this.renderer.setSize(window.innerWidth, window.innerHeight)
        document.body.appendChild(this.renderer.domElement)

        this.controls = new OrbitControls(this.camera, this.renderer.domElement)

        const texture = new THREE.TextureLoader().load( require("./../3d/airman.jpg") );
        const geometry = new THREE.BoxGeometry(10, 10, 10)
        const material = new THREE.MeshBasicMaterial({ map: texture})
        
        this.light = new THREE.DirectionalLight( 0xffffff, 1 );
        this.light.position.set( 0, -1, 0 );
        this.light.position.set( 13, 5, 0 );
        this.scene.add( this.light );
                
        this.gridXZ = new THREE.GridHelper(100, 10);
        this.cube = new THREE.Mesh(geometry, material)
        
        this.loader = new GLTFLoader();
        // this.loader.load(
        //     // resource URL
        //     'Parrot.glb',
        //     // called when the resource is loaded
        //     function ( gltf ) {

        //         this.scene.add( gltf.scene );

        //         gltf.animations; // Array<THREE.AnimationClip>
        //         gltf.scene; // THREE.Scene
        //         gltf.scenes; // Array<THREE.Scene>
        //         gltf.cameras; // Array<THREE.Camera>
        //         gltf.asset; // Object

        //     },
        //     // called while loading is progressing
        //     function ( xhr ) {

        //         console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );

        //     },
        //     // called when loading has errors
        //     function ( error ) {
                
        //         console.log( 'An error happened' );
        //         console.error(error)
        //     }
        // );
        this.loader.load('http://localhost:8081/testhom.glb', (gltf) => {
            const root = gltf.scene;
            console.log(gltf)
            this.scene.add(root);

            // // compute the box that contains all the stuff
            // // from root and below
            // const box = new THREE.Box3().setFromObject(root);

            // const boxSize = box.getSize(new THREE.Vector3()).length();
            // const boxCenter = box.getCenter(new THREE.Vector3());

            // // set the camera to frame the box
            // frameArea(boxSize * 0.5, boxSize, boxCenter, camera);

            // // update the Trackball controls to handle the new size
            // controls.maxDistance = boxSize * 10;
            // controls.target.copy(boxCenter);
            // controls.update();
        });

        // ----------------------------------- ORIGINAL ATTEMPT TO PORT BODY VISUALIZER -----------------------------------

        // HOMUNCULUS LOADING
        
        // this.character = new Character();
        // console.log("Character", this.character)
        // this.character.onLoadComplete = function() {
        //     console.log( "Load Complete" );
        //     console.log( this.character.numSkins + " skins and " + this.character.numMorphs + " morphtargets loaded." );
        //     this.gui = new dat.GUI();
        //     this.setupMorphsGUI();
        //     this.gui.width = 300;
        //     this.gui.open();
        // }
        
        // const JSONdata = testconfig
        // console.log("jsondata", JSONdata)

        
        // this.gui = new dat.GUI();
        // this.setupMorphsGUI();
        // this.gui.width = 300;
        // this.gui.open();


       
        // THis stuff below is fuckign shit

        // const request = new XMLHttpRequest()
        // console.log("processing request", request)
        // request.open('GET', "http://localhost:8081/public/models/skinned/testconfig.json", true)
        // request.addEventListener( 'load', function ( event ) {
        //     console.log("event")
        //     console.log(event)
        // })

        // console.log("env variable", process.env.VUE_APP_BASE_URL);
        
        // this.loader = new THREE.ObjectLoader();
        // this.loader.load("https://threejs.org/examples/models/gltf/Parrot.glb", function ( text ) {
            // https://srv-file9.gofile.io/download/QOnovt/testconfig.json
        // this.loader.load("/public/models/skinned/testconfig.json", function ( text ) {
        // this.loader.load("https://srv-file9.gofile.io/download/QOnovt/testconfig.json", function ( text ) {
        // this.loader.load("testconfig.json", function ( text ) {
        //     const config = JSON.parse( text );
        //     this.character.loadParts( config );
        //     this.scene.add( this.character.root );
        // } );

        // ----------------------------------- END OF ORIGINAL ATTEMPT TO PORT BODY VISUALIZER ----------------------------------

        this.scene.add(this.gridXZ);
        this.scene.add(this.cube)

        
        this.camera.position.set(10,13,10)
        this.controls.update()
        this.controls.enableZoom = true
        
        

        
        
    //   const animate = function() {}
    },
    setupMorphsGUI: function() {
				
        const morphGui = this.gui.addFolder( "Morphs" );
        
        const morphConfig = {};
        
        const morphCallback = function(  ) {
            return function () {
                this.character.updateMorphs( morphConfig );
            }
        }
        
        for ( var i = 0; i < this.character.numMorphs; i ++ ) {
            const morphName = this.character.morphs[ i ];
            
            morphConfig[ morphName ] = this.character.morphslimit[ i ];
            
        }
        
        for ( var j = 0; j < this.character.numMorphs; j ++ ) {
            
            morphGui.add( morphConfig, this.character.morphs[ j ] ).min(this.character.morphslowlimit[ j ] ).max(this.character.morphshighlimit[ j ]).onChange( morphCallback( j ) );
        }
        
        morphGui.open();
			
    },
    animate: function() {
        this.controls.update()
        requestAnimationFrame(this.animate)

        this.cube.rotation.x += 0.01
        this.cube.rotation.y += 0.01

        this.renderer.render(this.scene, this.camera)
    }
  },
  mounted() {
    // axios.get("testhom.glb")
    //     .then(response => {
    //     // JSON responses are automatically parsed.
    //         const testconfig = response.data
    //         // console.log("TEST CONFIG RESPONSE", testconfig)
    //     })
    //     .catch(e => {
    //         console.console.error(e);
            
    //     })
    this.init()
    this.animate()
  }
}
</script>