<script lang="ts">
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
	import { auth, fetchUser } from '$lib/stores/auth';
	import type { AuthState } from '$lib/stores/auth';
	
    export let skinName = '';
    let canvas : HTMLCanvasElement;
	let state: AuthState;
	$: $auth, state = $auth;

	const DANCING = 1;
	const MOVING = 2
	const TURN = 3

	onMount(() => { (async () => {
		await fetchUser()
		auth.subscribe((value : AuthState) =>{
            state = value;
        });
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera( 90, 2, 1, 1000 );
		scene.background = new THREE.Color(0x111111);

		var canvasSize = {width: window.innerWidth * 0.7,  height: window.innerWidth * 0.7 / 2 * 1}
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

		var top = renderer.domElement.getBoundingClientRect().top
		var	l = renderer.domElement.getBoundingClientRect().left
		var sphere = new THREE.Mesh(new THREE.SphereGeometry(0.1 , 5, 5), new THREE.MeshBasicMaterial( { color: 0xffcccc} ))

		camera.position.x = 0;
		camera.position.y = 0.8;
		camera.position.z = 1.7;

		var gloves = document.getElementById("gloves_ui");

		var ui = document.getElementById("ui");
		ui.style.width = canvasSize.width + "px";
		ui.style.height = canvasSize.height + "px";

		window.onresize = function(event){
			canvasSize.width = window.innerWidth * 0.7
			canvasSize.height = window.innerWidth * 0.7 / 2 * 1
			ui.style.width = canvasSize.width + "px";
       		ui.style.height = canvasSize.height + "px";
			top = renderer.domElement.getBoundingClientRect().top
			l = renderer.domElement.getBoundingClientRect().left
			renderer.setSize( canvasSize.width, canvasSize.height);
		}


		


		var left = rotating_skin.getObjectByName("Bone003L");
		var right = rotating_skin.getObjectByName("Bone003R");
		var bone = rotating_skin.getObjectByName("Bone");
		var animleg = 0;
		var dir = 0
		var dirx = 0
		var diry = 0

		const raycaster = new THREE.Raycaster()
		const clickmouse = new THREE.Vector2()
		const moveMouse = new THREE.Vector2()

		// window.addEventListener('mousemove', event => {
		// 	// gloves.style.top = (event.clientY - top) + "px"
		// 	// gloves.style.left = (event.clientX - l) + "px"
		// })
		scene.add(sphere)

		window.addEventListener('click', async(event) => {
			clickmouse.x = ((event.clientX - l) / renderer.domElement.clientWidth) * 2 - 1
			clickmouse.y = -(((event.clientY - top) / renderer.domElement.clientHeight) * 2 - 1)
			// gloves.style.top = (event.clientY - top) + "px"
			// gloves.style.left = (event.clientX - l) + "px"

			raycaster.setFromCamera( clickmouse, camera)
			const found = raycaster.intersectObjects(scene.children);
			if (found[0])
				sphere.position.set(found[0].point.x, found[0].point.y ,found[0].point.z );
		});

		function animateLegs(time : number) {

			if (dirx != 0)
				dir = Math.atan(diry / dirx);
			else
				dir = Math.asin(diry * 10 * 2 / 3);
			
			if (dirx == 0 && diry == 0)
				animleg = 0;
			else if (animleg == 0)
				animleg = Math.PI / 3;
			if (animleg != 0 && Math.abs(left.rotation.z) >= Math.abs(animleg) - 0.2)
				animleg *= -1;

			left.rotation.y = -dir;
			right.rotation.y = -dir;
			left.rotation.x = 0;
			right.rotation.x = 0;
			left.rotation.z = THREE.MathUtils.lerp(left.rotation.z, animleg, 0.1);
			right.rotation.z = THREE.MathUtils.lerp(right.rotation.z, animleg, 0.1);
			//bone.rotation.y = THREE.MathUtils.lerp(bone.rotation.y, dir / 8, 0.2);
			if (dirx < 0)
				dirx = 0;
			bone.rotation.x = THREE.MathUtils.lerp(bone.rotation.x, animleg / 10 + -dirx * 2, 0.1);
		}

		function animate() {
			requestAnimationFrame( animate );
			const dt = clock.getDelta();
			t += dt;
			renderer.render( scene, camera );
		}
		animate();
	})();
	});
</script>

<style>
	#ui {
        position: absolute;
		pointer-events: none;
		width: 10px;
		height: 10px;
		overflow: hidden;
    }

	#gloves {
		display: flex;
		justify-content: center;
		pointer-events: none;
		transform: translate(-50%);	
	}


	.glove {
		height: 300px;
		pointer-events: none;
		
	}

	#gloves_ui {
		position: absolute;
		display: flex;
		pointer-events: none;
		left: 50%;
		bottom: 0%;
	}

	#att_gloves_ui {
		position: absolute;
		display: inline;
		pointer-events: none;
		left: 50%;
		bottom: 0%;
	}

	.att_glove {
		display: none;
		position: absolute;
		bottom: 0;
  		right: 0;
	}

</style>

<div id="ui">
	<div id=gloves_ui>
		<div id="gloves">
			<img class="glove" src="/src/lib/assets/left_def_glove.png"/>
			<img class="glove"  src="/src/lib/assets/right_def_glove.png"/>
		</div>
	</div>
	<div id=att_gloves_ui>
		<img class="att_glove" src="/src/lib/assets/left_att_glove.png"/>
		<img class="att_glove"  src="/src/lib/assets/right_att_glove.png"/>
	</div>
</div>

<canvas bind:this={canvas} class=""></canvas>

