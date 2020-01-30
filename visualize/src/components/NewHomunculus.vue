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
    init() {

        this.state = {
            // environment: options.preset === Preset.ASSET_GENERATOR
            //     ? environments.find((e) => e.id === 'footprint-court').name
            //     : environments[1].name,
            background: false,
            playbackSpeed: 1.0,
            actionStates: {},
            // camera: DEFAULT_CAMERA,
            wireframe: false,
            skeleton: false,
            grid: false,

            // Lights
            addLights: true,
            exposure: 1.0,
            textureEncoding: 'sRGB',
            ambientIntensity: 0.3,
            ambientColor: 0xFFFFFF,
            directIntensity: 0.8 * Math.PI, // TODO(#116)
            directColor: 0xFFFFFF,
            bgColor1: '#ffffff',
            bgColor2: '#353535'
        };

        THREE.Cache.enabled = false;
        this.scene = new THREE.Scene()
        this.scene.background = new THREE.Color( 0x38374c );
        this.camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            2000
        )
        this.content = null;
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
        this.content = this.scene

        this.gridXZ = new THREE.GridHelper(100, 10);
        this.cube = new THREE.Mesh(geometry, material)
        
        this.loader = new GLTFLoader();
        this.loader.setCrossOrigin('anonymous');

        this.addGUI()
        this.updateGUI();
        console.log("morphfolder", this.morphFolder)
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
        
        //  window.content = this.content;
         console.log("window", window.content)
        

        
        
    //   const animate = function() {}
    },
    // setContent ( object, clips ) {

    //     this.clear();

    //     const box = new Box3().setFromObject(object);
    //     const size = box.getSize(new Vector3()).length();
    //     const center = box.getCenter(new Vector3());

    //     this.controls.reset();

    //     object.position.x += (object.position.x - center.x);
    //     object.position.y += (object.position.y - center.y);
    //     object.position.z += (object.position.z - center.z);
    //     this.controls.maxDistance = size * 10;
    //     this.defaultCamera.near = size / 100;
    //     this.defaultCamera.far = size * 100;
    //     this.defaultCamera.updateProjectionMatrix();

    //     if (this.options.cameraPosition) {

    //     this.defaultCamera.position.fromArray( this.options.cameraPosition );
    //     this.defaultCamera.lookAt( new Vector3() );

    //     } else {

    //     this.defaultCamera.position.copy(center);
    //     this.defaultCamera.position.x += size / 2.0;
    //     this.defaultCamera.position.y += size / 5.0;
    //     this.defaultCamera.position.z += size / 2.0;
    //     this.defaultCamera.lookAt(center);

    //     }

    //     this.setCamera(DEFAULT_CAMERA);

    //     this.axesCamera.position.copy(this.defaultCamera.position)
    //     this.axesCamera.lookAt(this.axesScene.position)
    //     this.axesCamera.near = size / 100;
    //     this.axesCamera.far = size * 100;
    //     this.axesCamera.updateProjectionMatrix();
    //     this.axesCorner.scale.set(size, size, size);

    //     this.controls.saveState();

    //     this.scene.add(object);
    //     this.content = object;

    //     this.state.addLights = true;

    //     this.content.traverse((node) => {
    //     if (node.isLight) {
    //         this.state.addLights = false;
    //     } else if (node.isMesh) {
    //         // TODO(https://github.com/mrdoob/three.js/pull/18235): Clean up.
    //         node.material.depthWrite = !node.material.transparent;
    //     }
    //     });

    //     // this.setClips(clips);

    //     // this.updateLights();
    //     this.updateGUI();
    //     this.updateEnvironment();
    //     // this.updateTextureEncoding();
    //     this.updateDisplay();

    //     window.content = this.content;
    //     console.info('[glTF Viewer] THREE.Scene exported as `window.content`.');
    //     this.printGraph(this.content);

    // },
    updateEnvironment() {
        console.log("update environment")
    },
    setupMorphsGUI() {
				
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
    addGUI() {
        this.gui = new dat.GUI({autoPlace: false, width: 260, hideable: true});
        console.log(this.gui)

        const dispFolder = this.gui.addFolder('Display');
        const wireframeCtrl = dispFolder.add(this.state, 'wireframe');
        wireframeCtrl.onChange(() => this.updateDisplay());
        // const dispFolder = gui.addFolder('Display');
        // const envBackgroundCtrl = dispFolder.add(this.state, 'background');
        // envBackgroundCtrl.onChange(() => this.updateEnvironment());
        // const wireframeCtrl = dispFolder.add(this.state, 'wireframe');
        // wireframeCtrl.onChange(() => this.updateDisplay());
        // const skeletonCtrl = dispFolder.add(this.state, 'skeleton');
        // skeletonCtrl.onChange(() => this.updateDisplay());
        // const gridCtrl = dispFolder.add(this.state, 'grid');
        // gridCtrl.onChange(() => this.updateDisplay());
        // dispFolder.add(this.controls, 'autoRotate');
        // dispFolder.add(this.controls, 'screenSpacePanning');
        // // const bgColor1Ctrl = dispFolder.addColor(this.state, 'bgColor1');
        // // const bgColor2Ctrl = dispFolder.addColor(this.state, 'bgColor2');
        // // bgColor1Ctrl.onChange(() => this.updateBackground());
        // // bgColor2Ctrl.onChange(() => this.updateBackground());


        // Morph target controls.
        this.morphFolder = this.gui.addFolder('Morph Targets');
        this.morphFolder.domElement.style.display = 'none';

        const guiWrap = document.createElement('div');
        // this.el.appendChild( guiWrap );
        guiWrap.classList.add('gui-wrap');
        guiWrap.appendChild(this.gui.domElement);
        this.gui.open();

    },
    updateDisplay() {
        console.log("update display")
    },
    updateGUI() {
        this.morphCtrls.forEach((ctrl) => ctrl.remove());
        this.morphCtrls.length = 0;
        this.morphFolder.domElement.style.display = 'none';

        const morphMeshes = [];

        this.content.traverse((node) => {
            console.log("node", node)
            if (node.isMesh && node.morphTargetInfluences) {
                morphMeshes.push(node);
            }
        });

        console.log("morphMeshes", morphMeshes)

        if (morphMeshes.length) {
            this.morphFolder.domElement.style.display = '';
            morphMeshes.forEach((mesh) => {
                if (mesh.morphTargetInfluences.length) {
                    const nameCtrl = this.morphFolder.add({name: mesh.name || 'Untitled'}, 'name');
                    this.morphCtrls.push(nameCtrl);
                }
                for (let i = 0; i < mesh.morphTargetInfluences.length; i++) {
                    const ctrl = this.morphFolder.add(mesh.morphTargetInfluences, i, 0, 1, 0.01).listen();
                    Object.keys(mesh.morphTargetDictionary).forEach((key) => {
                        if (key && mesh.morphTargetDictionary[key] === i) ctrl.name(key);
                    });
                    this.morphCtrls.push(ctrl);
                }
            });
        }
    },
    animate() {
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