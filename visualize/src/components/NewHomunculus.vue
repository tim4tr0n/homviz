<template>
  <div id="container"></div>
</template>
<script>
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import * as dat from 'dat.gui';
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
        
        this.morphCtrls = [];
        this.morphFolder = null;
        this.renderer = new THREE.WebGLRenderer()
        this.renderer.setSize(window.innerWidth, window.innerHeight)
        document.body.appendChild(this.renderer.domElement)

        this.controls = new OrbitControls(this.camera, this.renderer.domElement)

        const texture = new THREE.TextureLoader().load( require("./../3d/airman.jpg") );
        const geometry = new THREE.BoxGeometry(10, 10, 10)
        const material = new THREE.MeshBasicMaterial({ map: texture, wireframe: true })
        

        this.light = new THREE.DirectionalLight( 0xffffff, 1 );
        this.light.position.set( 0, -1, 0 );
        this.light.position.set( 13, 5, 0 );
        this.scene.add( this.light );
                
        this.gridXZ = new THREE.GridHelper(100, 10);
        this.cube = new THREE.Mesh(geometry, material)
        
        this.loader = new GLTFLoader();
        this.   loader.setCrossOrigin('anonymous');
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
            // called while loading is progressing
            // function ( xhr ) {

            //     console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );

            // },
        //     // called when loading has errors
        //     function ( error ) {
                
        //         console.log( 'An error happened' );
        //         console.error(error)
        //     }
        // );
        this.loader.load(
            'http://localhost:8081/guy.gltf',
            (gltf) => {
                const root = gltf.scene;
                console.log(gltf)
                gltf.scene.scale.set(10,10,10)
                this.scene.add(root);

                root.position.set(0,0,0)
            },
            // called while loading is progressing
            ( xhr ) => {
                console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );

            },
            // called when loading has errors
            ( error ) => {
                console.log( 'An error happened' );
                console.error(error)
            }
        
        );

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

        
        this.camera.position.set(10,20,26)
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
    addGUI: function() {
        const gui = this.gui = new dat.GUI({autoPlace: false, width: 260, hideable: true});

        const dispFolder = gui.addFolder('Display');
        const envBackgroundCtrl = dispFolder.add(this.state, 'background');
        envBackgroundCtrl.onChange(() => this.updateEnvironment());
        const wireframeCtrl = dispFolder.add(this.state, 'wireframe');
        wireframeCtrl.onChange(() => this.updateDisplay());
        const skeletonCtrl = dispFolder.add(this.state, 'skeleton');
        skeletonCtrl.onChange(() => this.updateDisplay());
        const gridCtrl = dispFolder.add(this.state, 'grid');
        gridCtrl.onChange(() => this.updateDisplay());
        dispFolder.add(this.controls, 'autoRotate');
        dispFolder.add(this.controls, 'screenSpacePanning');
        // const bgColor1Ctrl = dispFolder.addColor(this.state, 'bgColor1');
        // const bgColor2Ctrl = dispFolder.addColor(this.state, 'bgColor2');
        // bgColor1Ctrl.onChange(() => this.updateBackground());
        // bgColor2Ctrl.onChange(() => this.updateBackground());


        // Morph target controls.
        this.morphFolder = gui.addFolder('Morph Targets');
        this.morphFolder.domElement.style.display = 'none';

    },
    updateDisplay: function() {
        console.log("update display")
    },
    updateGui: function() {
        this.morphCtrls.forEach((ctrl) => ctrl.remove());
        this.morphCtrls.length = 0;
        this.morphFolder.domElement.style.display = 'none';
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
    this.addGUI()
    this.animate()
  }
}
</script>