<script lang="ts">
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';;
	import { Player } from "./player.js";
	import { Bot } from "./bot.js";
	import { shade } from "./watershader";

	let canvas;
	var scoring = 0;

	onMount(() => { (async () => {

		var skin = ""
		const response = await fetch('api/user/game_data/', {
		method: 'GET',
		headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
		});
		const data = await response.json();
		if (response.ok)
		{
			skin = data.skin
		}



		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.1, 1000 );
		scene.background = new THREE.Color(0x54A0E4);

		
		var bind = {up: 90, down: 83, left:81, right:68, charge:32}
		//var bind2 = {up: 38, down: 40, left:37, right:39, charge:96}
		var limit = {px: 0, py:8, nx:-18, ny:-8}
		var limit2 = {px: 18, py:8, nx: 0, ny:-8}
		var scores = [0, 0];
		var bots = [];
		var id = 0;
		var ui = document.getElementById("ui");
		var score1 = document.getElementById("player1")
		var score2 = document.getElementById("player2")
		
		var endscoring = 0;

		const uppertribune = new THREE.Mesh(new THREE.PlaneGeometry(34, 1), new THREE.MeshStandardMaterial);
		uppertribune.position.set(0, 9, -0.5);

		const lowertribune = new THREE.Mesh(new THREE.PlaneGeometry(34, 1), new THREE.MeshStandardMaterial);
		lowertribune.position.set(0, -9, -0.5);

		const righttribune = new THREE.Mesh(new THREE.PlaneGeometry(1, 14), new THREE.MeshStandardMaterial);
		righttribune.position.set(17, 0, -0.5);

		const lefttribune = new THREE.Mesh(new THREE.PlaneGeometry(1, 14), new THREE.MeshStandardMaterial);
		lefttribune.position.set(-17.5, 0, -0.5);
		const collisions = [righttribune, uppertribune, lefttribune, lowertribune];

		//#region LoadModel

		const loader = new GLTFLoader()


		const g = await loader.loadAsync('src/lib/assets/skins/vazy.glb');

		let i = 0;
		g.scene.scale.set(0.5, 0.5, 0.5);
		while (i < 4)
		{
			bots.push(new Bot(g.scene, collisions));
			scene.add(bots[i].mesh);
			i ++;
		}

		const gltf = await loader.loadAsync('src/lib/assets/skins/' + skin);

		gltf.scene.position.set(-25, 0, -0.8);
		gltf.scene.scale.set(0.5, 0.5, 0.5);


		gltf.scene.position.set(-10, 0, -1.5);
		gltf.scene.scale.set(0.5, 0.5, 0.5);
		gltf.scene.rotation.y = Math.PI / 2;
		gltf.scene.rotation.x = Math.PI / 2;

		var play = new Player(gltf, bind, limit, 0.15, 1);
		scene.add(play.mesh);




		const gl = await loader.loadAsync('src/lib/assets/skins/vazy.glb');

		gl.scene.position.set(10, 0, -1.5);
		gl.scene.scale.set(0.5, 0.5, 0.5);
		gl.scene.rotation.y = Math.PI * 3 / 2;
		gl.scene.rotation.x = Math.PI / 2;

		var er = new Player(gl, bind, limit2, 0.15, -1);
		scene.add(er.mesh);




	
		const bouee = await loader.loadAsync('src/routes/pong/public/bue.glb');
		bouee.scene.position.set(0, -9, -0.8);
		bouee.scene.rotation.x = Math.PI / 2
		bouee.scene.rotation.y = Math.PI / 2

		scene.add(bouee.scene);

		//#endregion


		//#region CreateMesh

		const geo = new THREE.SphereGeometry( 0.8, 32, 16); 
		const mat = new THREE.MeshStandardMaterial( { color: 0xffc200 } ); 
		const sphere = new THREE.Mesh( geo, mat );
		scene.add( sphere );

		let spherebb = new THREE.Sphere(sphere.position, 1);



		const plain = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), shade);

		plain.position.set(0, 0, -0.8);
		plain.overdraw = true;
		plain.receiveShadow = true;

		scene.add(plain);

		//#endregion


		const light = new THREE.AmbientLight(0xffffff)
		scene.add(light)

		const dl = new THREE.DirectionalLight( 0xffffff, 2 );
		dl.position.set( 0, 0, 5 );
		scene.add( dl );

		const renderer = new THREE.WebGLRenderer({canvas, antialias: false});
		renderer.setSize( window.innerWidth * 0.70, (window.innerWidth * 0.70) / 16 * 9);
        ui.style.width = window.innerWidth * 0.7 + "px";
        ui.style.height = (window.innerWidth * 0.70) / 16 * 9 + "px";
        ui.style.top = renderer.domElement.getBoundingClientRect().top + "px"
        ui.style.left = renderer.domElement.getBoundingClientRect().left + "px"
		renderer.shadowMap.enabled = true;
		document.body.appendChild( renderer.domElement );

		camera.position.z = 20;

		var xSpeed = 0.15;
		var ySpeed = 0.15;


		var ballspeed = 0.2;


		//#region CommandHandler

		document.addEventListener("keydown", onDocumentKeyDown, false);
		document.addEventListener("keyup", onDocumentKeyUp, false);

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
			renderer.setSize( window.innerWidth * 0.70, (window.innerWidth * 0.70) / 16 * 9);
            ui.style.width = window.innerWidth * 0.7 + "px";
            ui.style.height = (window.innerWidth * 0.70) / 16 * 9 + "px";
            ui.style.top = renderer.domElement.getBoundingClientRect().top + "px"
            ui.style.left = renderer.domElement.getBoundingClientRect().left + "px"
		}

		function onDocumentKeyDown(event) {
			var keyCode = event.which;
			play.keydown(keyCode)
			er.keydown(keyCode)
		};

		function onDocumentKeyUp(event) {
			var keyCode = event.which;
			play.keyup(keyCode)
			er.keyup(keyCode)
		};
		//#endregion

		let t = 0;
		const clock = new THREE.Clock();

		let balldir = -0.1;
		let balldiry = 0


		//#endregion

		//#region Collision

		function checkCollision() {
			if (er.bb.intersectsSphere(spherebb) && er.charge == 0)
			{
				if (balldir > 1)
					er.knockback = -0.4;
				balldir = -0.5 * er.charging;
				balldiry = (sphere.position.y - er.mesh.position.y) * 0.1;
			}
			if (play.bb.intersectsSphere(spherebb) && play.charge == 0)
			{
				if (balldir < -1)
					play.knockback = -0.4;
				balldir = 0.5 * play.charging;
				balldiry = (sphere.position.y - play.mesh.position.y) * 0.1;
			}
			if (balldir < 0)
			{
				balldir = THREE.MathUtils.lerp(balldir, -ballspeed, 0.05 );
			}
			if (balldir > 0)
			{
				balldir = THREE.MathUtils.lerp(balldir, ballspeed, 0.05);
			}
		}

		var frames = 0
		let url = '/ws/pong/pong/' + localStorage.getItem('room_name') + '/?token=' + localStorage.getItem('access_token');
		const chatSocket = new WebSocket(url)

		chatSocket.onmessage = function(e) {
	
			let data = JSON.parse(e.data)
			if (data.event == 'Connected')
			{
				console.log('connected')
				id = data.id
				if (id == 1)
				{
				chatSocket.send(JSON.stringify({
					'event':'frame',
					'player1':play.controller,
				}))
				}
				if (id == 2)
				{
				chatSocket.send(JSON.stringify({
					'event':'frame',
					'player2':er.controller,
				}))
				}
			}
			else if (data.event == 'frame')
			{
				play.mesh.position.set(data.player1[0], data.player1[1], -1.5)
				er.mesh.position.set(data.player2[0], data.player2[1], -1.5)
				if (data.player1[2] != scores[0])
				{
					scores[0] = data.player1[2]
					score1.textContent = scores[0].toString()
				}
				if (data.player2[2] != scores[1])
				{
					scores[1] = data.player2[2]
					score2.textContent = scores[1].toString()
				}
				play.controllanims = data.player1[3]
				er.controllanims = data.player2[3]
				sphere.position.set(data.ball, data.bally, sphere.position.z);
				scoring = data.scoring
				if (id == 1)
				{
					chatSocket.send(JSON.stringify({
						'event':'frame',
						'player1':play.controller,
					}))
				}
				if (id == 2)
				{
					chatSocket.send(JSON.stringify({
						'event':'frame',
						'player2':er.controller,
					}))
				}
			}
		}

		//#endregion

		//var composer = new EffectComposer( renderer );
		//composer.addPass( new RenderPass( scene, camera ) );

		/*var afterimagePass = new AfterimagePass();
		composer.addPass( afterimagePass );*/


		//var renderPixelatedPass = new RenderPixelatedPass( 2, scene, camera );
		//composer.addPass( renderPixelatedPass );

		function animate() {
			requestAnimationFrame( animate );
			const dt = clock.getDelta();
			plain.material.uniforms.time.value = t * 70;
			t += dt;
			if (gamepads[0])
			{
				gamepads[0] = navigator.getGamepads()[0]
				handlebuttons(gamepads[0].buttons)
				handlesticks(gamepads[0].axes)
			}
			play.update(dt)
			er.update(dt)

			bots.forEach(element => {
				element.update();
				element.scoring = scoring;
			});
			frames ++;
			checkCollision();
			renderer.render( scene, camera );
		}
		animate();
	})();
	});
</script>

<style>
	/*@import url('https://fonts.googleapis.com/css2?family=Lilita+One&display=swap');*/
	@import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');
    #ui {
        position: absolute;
		width: 10px;
		height: 10px;

    }

	#score {
		position: absolute;
		width: 100%;
		height: 100%;
		display:flex;
		justify-content: space-evenly;
	}

	.game {
        margin: auto !important;
    }

	.text {
		/*font-family: "Lilita One", sans-serif;*/
		font-family: "Luckiest Guy", cursive;
  		font-weight: 400;
  		font-style: normal;
		color:white;
		font-size: 70px;
		text-shadow:
		2px 2px 0 #000,
		-2px 2px 0 #000,
		-2px -2px 0 #000,
		2px -2px 0 #000;
	}




</style>

<div id="ui">
	<div id="score">
		<span class="text" id="player1">0</span>
		<span class="text" id="player2">0</span>
	</div>
</div>


<canvas bind:this={canvas} class="game"></canvas>

