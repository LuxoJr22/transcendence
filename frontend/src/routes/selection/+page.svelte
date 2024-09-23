<script lang= "ts">
    import { Bot } from "./bot";
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
	import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
	import { SkeletonCollider } from "./skeletoncollider.js"
	let canvas;

	onMount(() => { (async () => {
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.1, 1000 );
		scene.background = new THREE.Color(0xCCCCCC);



		var t = 0;
		const clock = new THREE.Clock();

		const loader = new GLTFLoader()

		var bots = [];


		const gltf = await loader.loadAsync('src/routes/selection/public/pop.glb');
		bots.push(new Bot(gltf.scene, scene))


		const gm = await loader.loadAsync('src/routes/selection/public/sty.glb');
		bots.push(new Bot(gm.scene, scene))

		gm.scene.position.set(10, 0, 0)

		const dd = await loader.loadAsync('src/routes/selection/public/pir.glb');
		bots.push(new Bot(dd.scene, scene))

		dd.scene.position.set(-10, 0, 0)




		var texture = new THREE.TextureLoader().load( 'src/routes/selection/public/floor.png' );
		texture.wrapS = THREE.RepeatWrapping;
		texture.wrapT = THREE.RepeatWrapping;
		texture.repeat.set( 4, 4 );

		var mat = new THREE.MeshStandardMaterial( { map : texture})
		const plain = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), mat);
		plain.rotation.x = -Math.PI / 2
		scene.add(plain)
		plain.name = "floor"
		


		const light = new THREE.AmbientLight(0xffffff)
		scene.add(light)

		const dl = new THREE.DirectionalLight( 0xffffff, 2 );
		dl.position.set( 0, 5, 0 );
		scene.add( dl );

		const renderer = new THREE.WebGLRenderer({canvas, antialias: false});
		renderer.setSize( 1920 * 0.7 , 1080 * 0.7);
		renderer.shadowMap.enabled = true;
		document.body.appendChild( renderer.domElement );
		var top = renderer.domElement.getBoundingClientRect().top


		//const controls = new OrbitControls( camera, renderer.domElement );
		//controls.update();


		camera.position.z = 20;
		camera.position.y = 30;
		camera.rotation.x = -Math.PI / 3.5

		const plan = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), mat);
		plan.position.y = 24
		plan.rotation.x = -Math.PI / 3.5
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
			if (window.innerWidth * 0.7 < 1920 * 0.7)
				renderer.setSize( window.innerWidth * 0.70, (window.innerWidth * 0.70) / 16 * 9);
			top = renderer.domElement.getBoundingClientRect().top
		}


		
		const raycaster = new THREE.Raycaster()
		const clickmouse = new THREE.Vector2()
		const moveMouse = new THREE.Vector2()
		var draggable = null

		window.addEventListener('click', event => {
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

					draggable = null
				}

				
				return
			}
			clickmouse.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1
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
						bots[i].ispicked = 1
					}
					i++
				}
			}
		})

		window.addEventListener('mousemove', event => {
			moveMouse.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1
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
							draggable.mesh.position.z = THREE.MathUtils.lerp(draggable.mesh.position.z, o.point.z, 0.1)
							draggable.mesh.position.y = THREE.MathUtils.lerp(draggable.mesh.position.y, o.point.y, 0.1)
							draggable.mesh.rotation.y = THREE.MathUtils.lerp(draggable.mesh.rotation.y, 0, 0.1)
							draggable.mesh.rotation.x = THREE.MathUtils.lerp(draggable.mesh.rotation.x, -Math.PI / 3.5, 0.1)
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

<canvas bind:this={canvas} class=""></canvas>