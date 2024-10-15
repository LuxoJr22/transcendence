<script lang="ts">
    import { Bot } from "./bot";
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
	import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
	import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';
	import { SkeletonCollider } from "./skeletoncollider.js"
	import { auth } from '$lib/stores/auth';
	import type { AuthState } from '$lib/stores/auth';

	let state: AuthState;
	$: $auth, state = $auth;

	let canvas;

	onMount(() => { (async () => {
		auth.subscribe((value : AuthState) =>{
            state = value;
        });
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera( 70, 16 / 9, 0.1, 1000 );
		scene.background = new THREE.Color(0xCCCCCC);
		var canvasSize = {width: window.innerWidth * 0.7,  height: window.innerWidth * 0.7 / 16 * 9}

		var game = document.getElementById("gameCanvas");
		var ui = document.getElementById("ui")
		var whistle = document.getElementById("whistle")

		var t = 0;
		const clock = new THREE.Clock();

		const loader = new GLTFLoader()

		var bots = [];

		const pop = await loader.loadAsync('src/lib/assets/skins/vazy.glb');
		pop.scene.scale.set(0.5, 0.5, 0.5);
		pop.scene.position.set(0, 0, 8)
		bots.push(new Bot(pop, scene, 'vazy.glb'))


		const gentleman = await loader.loadAsync('src/lib/assets/skins/gentleman.glb');
		gentleman.scene.scale.set(0.5, 0.5, 0.5);
		gentleman.scene.position.set(5, 0, 8)
		bots.push(new Bot(gentleman, scene, 'gentleman.glb'))

		const pirate = await loader.loadAsync('src/lib/assets/skins/pirate.glb');
		pirate.scene.scale.set(0.5, 0.5, 0.5);
		pirate.scene.position.set(-5, 0, 8)
		bots.push(new Bot(pirate, scene, 'pirate.glb'))
		

		const def = await loader.loadAsync('src/lib/assets/skins/default.glb');
		def.scene.scale.set(0.5, 0.5, 0.5);
		def.scene.position.set(-10, 0, 8)
		bots.push(new Bot(def, scene, 'default.glb'))
		var rotating_skin : THREE.Object3D;

		bots.forEach(el => {
			if (el.name == state.user.skin)
			{
				rotating_skin = SkeletonUtils.clone(el.mesh);
				rotating_skin.getObjectByName("Bone003L").rotation.set(0, 0, 0);
				rotating_skin.getObjectByName("Bone003R").rotation.set(0, 0, 0);
				rotating_skin.getObjectByName("Bone").rotation.set(0, 0, 0);
				rotating_skin.position.set(-8, 5, 20)
				rotating_skin.rotation.set( -Math.PI / 3, 0, 0)
				rotating_skin.scale.set(0.3, 0.3, 0.3);
				scene.add(rotating_skin)
			}
		})
		
		

		var texture = new THREE.TextureLoader().load( 'src/routes/(private)/selection/public/floor.png' );
		texture.wrapS = THREE.RepeatWrapping;
		texture.wrapT = THREE.RepeatWrapping;
		texture.repeat.set( 4, 4 );

		var mat = new THREE.MeshStandardMaterial( { map : texture})
		const plain = new THREE.Mesh(new THREE.PlaneGeometry(100, 50), mat);
		plain.position.x = 12.5
		plain.rotation.x = -Math.PI / 2
		scene.add(plain)
		plain.name = "floor"
		


		const light = new THREE.AmbientLight(0xffffff)
		scene.add(light)

		const dl = new THREE.DirectionalLight( 0xffffff, 1.5);
		dl.position.set( 0, 5, 0 );
		scene.add( dl );

		const renderer = new THREE.WebGLRenderer({canvas, antialias: false});
		renderer.setSize( canvasSize.width, canvasSize.height);
		ui.style.width = canvasSize.width + "px";
        ui.style.height = canvasSize.height + "px";
        ui.style.top = renderer.domElement.getBoundingClientRect().top + "px"
        ui.style.left = renderer.domElement.getBoundingClientRect().left + "px"
		var top = renderer.domElement.getBoundingClientRect().top
		var left = renderer.domElement.getBoundingClientRect().left
		renderer.shadowMap.enabled = true;
		document.body.appendChild( renderer.domElement );
		


		camera.position.z = 20;
		camera.position.y = 15;
		camera.rotation.x = -Math.PI / 3

		const plan = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), mat);
		plan.position.y = 16
		plan.rotation.x = -Math.PI / 3
		plan.name = "frontplane"
		scene.add(plan)
		plan.visible = false

		const gamepads = {};

		function gamepadHandler(event, connected) {
		const gamepad = event.gamepad;

		if (connected) {
			gamepads[gamepad.index] = gamepad;
		} else {
			delete gamepads[gamepad.index];
		}
		}

		function handlebuttons(buttons)
		{
			if (buttons[0].value > 0)
				play.controller.charge = 1;
			if (buttons[0].value == 0)
				play.controller.charge = 0;
		}

		var xSpeed = 0.15, ySpeed = 0.15;

		function handlesticks(axes)
		{
			if (axes[0] < -0.2)
				play.controller.xn = axes[0] * xSpeed;
			else
				play.controller.xn = 0;
			if (axes[0] > 0.2)
				play.controller.xp = axes[0] * xSpeed;
			else
				play.controller.xp = 0;

			if (axes[1] < -0.2)
				play.controller.yn = -axes[1] * ySpeed;
			else
				play.controller.yn = 0;
			if (axes[1] > 0.2)
				play.controller.yp = -axes[1] * ySpeed;
			else
				play.controller.yp = 0;
		}

		window.addEventListener(
		"gamepadconnected",
		(e) => {
			gamepadHandler(e, true);
		},
		false,
		);

		window.addEventListener(
		"gamepaddisconnected",
		(e) => {
			gamepadHandler(e, false);
		},
		false,
		);

		window.onresize = function(event){
			canvasSize.width = window.innerWidth * 0.7
			canvasSize.height = window.innerWidth * 0.7 / 16 * 9
			renderer.setSize( canvasSize.width, canvasSize.height);
			ui.style.width = canvasSize.width + "px";
        	ui.style.height = canvasSize.height + "px";
        	ui.style.top = renderer.domElement.getBoundingClientRect().top + "px"
        	ui.style.left = renderer.domElement.getBoundingClientRect().left + "px"
			top = renderer.domElement.getBoundingClientRect().top
			left = renderer.domElement.getBoundingClientRect().left
		}


		
		const raycaster = new THREE.Raycaster()
		const clickmouse = new THREE.Vector2()
		const moveMouse = new THREE.Vector2()
		var draggable = null

		whistle.addEventListener('click', (e) => {
			var i = 0
			while (bots[i])
			{
				bots[i].moving = 0;
				bots[i].throwed = 0;
				bots[i].iscalled = 1;
				bots[i].mesh.rotation.y = 0
				let destx = i * 5 - ((bots.length - 1) * 5 / 2)
				let hypo = Math.sqrt(Math.pow(bots[i].mesh.position.x - destx, 2) + Math.pow(bots[i].mesh.position.z - 8, 2))
				let scal = 8 - bots[i].mesh.position.z
				let angle = Math.acos(scal / ( hypo))
				if (hypo == 0)
					angle = 0
				bots[i].mesh.rotation.y = angle
				if (destx - bots[i].mesh.position.x < 0)
					bots[i].mesh.rotation.y *= -1
				if (destx - bots[i].mesh.position.x == 0 && 8 - bots[i].mesh.position.z < 0 )
					bots[i].mesh.rotation.y *= -1
				bots[i].dest = [i * 5 - ((bots.length - 1) * 5 / 2), 0, 8]
				i ++
			}
		})

		window.addEventListener('click', async(event) => {
			if (draggable)
			{
				
				const found = raycaster.intersectObjects(scene.children);
				var i = 0;
				var drop = 0
				while (found[i] && drop == 0)
				{
					if (found[i].object.name == "floor")
						drop = 1
					else
						i ++;
				}
				if (drop == 1)
				{
					draggable.ispicked = 0;
					draggable.throwed = 1;
					draggable.targetx = found[i].point.x 
					draggable.targetz = found[i].point.z
					draggable.moving = 0;
					ui.style.cursor = "url('src/routes/(private)/selection/public/hand.png'), auto";

					draggable = null
				}

				
				return
			}
			clickmouse.x = ((event.clientX - left) / renderer.domElement.clientWidth) * 2 - 1
			clickmouse.y = -(((event.clientY - top) / renderer.domElement.clientHeight) * 2 - 1)

			raycaster.setFromCamera( clickmouse, camera)
			const found = raycaster.intersectObjects(scene.children);
			if (found.length > 1)
			{
				var obj = found[1].object
				var i = 0
				while (bots[i])
				{
					if (bots[i].target.includes(obj))
					{
						
						draggable = bots[i]
						ui.style.cursor = "url('src/routes/(private)/selection/public/closedHand.png'), auto";
						draggable.throwed = 0 
						bots[i].ispicked = 1
						const response = await fetch('/api/user/skin/update/', {
							method: 'PATCH',
							headers: { 'Content-Type':'application/json','Authorization': `Bearer ${localStorage.getItem('access_token')}` },
							body: JSON.stringify({
								"skin": bots[i].name
							})
						});
						scene.remove(rotating_skin)
						rotating_skin = SkeletonUtils.clone(bots[i].mesh);
						rotating_skin.getObjectByName("Bone003L").rotation.set(0, 0, 0);
						rotating_skin.getObjectByName("Bone003R").rotation.set(0, 0, 0);
						rotating_skin.getObjectByName("Bone").rotation.set(0, 0, 0);
						rotating_skin.position.set(-8, 5, 20)
						rotating_skin.rotation.set( -Math.PI / 3, 0, 0)
						rotating_skin.scale.set(0.3, 0.3, 0.3);
						scene.add(rotating_skin)
					}
					i++
				}
			}
		})

		window.addEventListener('mousemove', event => {
			moveMouse.x = ((event.clientX - left) / renderer.domElement.clientWidth) * 2 - 1
			moveMouse.y = -(((event.clientY - top) / renderer.domElement.clientHeight) * 2 - 1)
		})

		function dragObject() {
			if (draggable != null) {
				raycaster.setFromCamera(moveMouse, camera)
				const found = raycaster.intersectObjects(scene.children)
				if (found.length > 0){
					for (let o of found) {
						if (o.object.name == "frontplane"){
							draggable.mesh.position.x = THREE.MathUtils.lerp(draggable.mesh.position.x, o.point.x, 0.1)
							draggable.mesh.position.z = THREE.MathUtils.lerp(draggable.mesh.position.z, o.point.z + 1, 0.1)
							draggable.mesh.position.y = THREE.MathUtils.lerp(draggable.mesh.position.y, o.point.y - 1, 0.1)
							draggable.mesh.rotation.y = THREE.MathUtils.lerp(draggable.mesh.rotation.y, 0, 0.1)
							draggable.mesh.rotation.x = THREE.MathUtils.lerp(draggable.mesh.rotation.x, -Math.PI / 6, 0.1)
						}
					}
				}
			}
		}
		function animate() {
			dragObject()
			requestAnimationFrame( animate );
			//controls.update();
			const dt = clock.getDelta();
			t += dt;
			bots.forEach(element => {
				element.update(dt, t);
			});
			if (rotating_skin)
				rotating_skin.rotation.y += 0.2 * dt
			if (gamepads[0])
			{
				gamepads[0] = navigator.getGamepads()[0]
				handlebuttons(gamepads[0].buttons)
				handlesticks(gamepads[0].axes)
			}
			frames ++;
			renderer.render( scene, camera );
		}
		animate();
	})();
	});
</script>

<style>
	#ui {
        position: absolute;
		width: 10px;
		height: 10px;
		cursor: url("src/routes/(private)/selection/public/hand.png"), auto;
    }


	#whistle {
		display: block;
		position: relative;
		max-width:10%;
		top: 75%;
		left: 85%
	}

	#whistle >img {
		display: block !important;
		position: relative;
		height: 100%;
		width: 100%;
		/* transform: translate(-50%, 50%); */
	}

	.game {
	        /*border-radius: 3% !important;*/
	        margin: auto !important;

	    }
	#gameCanvas {
		cursor: url("src/routes/(private)/selection/public/hand.png"), auto;
	}
</style>

<div id="ui">
	<div id="whistle">
		<img src="src/routes/(private)/selection/public/whistle4.png"/>
	</div>
</div>

<canvas bind:this={canvas} class="d-flex flex-column game" id="gameCanvas"></canvas>