<script lang="ts">
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
    import {  userData } from '$lib/stores/user';
	import { auth, fetchUser } from '$lib/stores/auth';
	import type { AuthState } from '$lib/stores/auth';

    let canvas : HTMLCanvasElement;
	let skinName = '';
	export let self;
	export let userId = 0;

	onMount(() => { (async () => {
		if (self){
			await fetchUser();
			auth.subscribe((value : AuthState) =>{
            	skinName = value.user!.skin;
        	});
		}
		else {
			const data : any = await userData(userId);
            skinName = data.skin;
		}
		
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera( 90, 1, 0.1, 1000 );
		scene.background = new THREE.Color(0x212529);
		var canvasSize = {width: window.innerWidth * 0.1,  height: window.innerWidth * 0.1}
		var t = 0;
		const clock = new THREE.Clock();
		const loader = new GLTFLoader()
		const skin = await loader.loadAsync('/src/lib/assets/skins/' + skinName);
        var rotating_skin : THREE.Object3D;
        rotating_skin = skin.scene;
		rotating_skin.scale.set(0.3, 0.3, 0.3);
		scene.add(rotating_skin)
		const light = new THREE.AmbientLight(0xffffff)
		scene.add(light)
		const dl = new THREE.DirectionalLight( 0xffffff, 1.5);
		dl.position.set( 0, 0.8, 1.7 );
		scene.add( dl );
		const renderer = new THREE.WebGLRenderer({canvas, antialias: false});
		renderer.setSize( canvasSize.width, canvasSize.height);
		renderer.shadowMap.enabled = true;
		camera.position.x = 0;
		camera.position.y = 0.8;
		camera.position.z = 1.7;
		window.onresize = function(event){
			canvasSize.width = window.innerWidth * 0.1
			canvasSize.height = window.innerWidth * 0.1
			renderer.setSize( canvasSize.width, canvasSize.height);
		}
		function animate() {
			requestAnimationFrame( animate );
			const dt = clock.getDelta();
			t += dt;
			if (rotating_skin)
				rotating_skin.rotation.y += 0.2 * dt
			renderer.render( scene, camera );
		}
		animate();
	})();
	});
</script>

<canvas bind:this={canvas} class=""></canvas>

