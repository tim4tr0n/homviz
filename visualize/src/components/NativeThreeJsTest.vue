<template>
  <div id="container"></div>
</template>
<script>
import * as THREE from 'three'

export default {
  name: 'ThreeTest',
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
        this.scene = new THREE.Scene()
        this.camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        )
        
        var light = new THREE.DirectionalLight( 0xffffff, 1 );
        light.position.set( 0, -1, 0 );
        light.position.set( 13, 5, 0 );
        this.scene.add( light );
        

        this.renderer = new THREE.WebGLRenderer()
        this.renderer.setSize(window.innerWidth, window.innerHeight)
        document.body.appendChild(this.renderer.domElement)

        var controls = new THREE.OrbitControls( this.camera, this.renderer.domElement );

        const geometry = new THREE.BoxGeometry(1, 1, 1)
        const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 })
        this.cube = new THREE.Mesh(geometry, material)
        this.scene.add(this.cube)

        this.camera.position.z = 5
        controls.update()
    //   const animate = function() {}
    },
    animate: function() {
        requestAnimationFrame(this.animate)

        this.cube.rotation.x += 0.01
        this.cube.rotation.y += 0.01

        this.renderer.render(this.scene, this.camera)
    }
  },
  mounted() {
    this.init()
    this.animate()
  }
}
</script>