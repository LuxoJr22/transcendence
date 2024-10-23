<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import * as THREE from 'three';
	import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
	import { Player } from "$lib/stores/pong/player";
	import { Bot } from "$lib/stores/pong/bot";
	import { shade } from "$lib/stores/pong/watershader";
	import { Firework } from '$lib/stores/pong/firework';
	import { auth, getAccessToken } from '$lib/stores/auth';
	import type { AuthState } from '$lib/stores/auth';
	import { goto } from '$app/navigation';

	let state: AuthState;
	$: $auth, state = $auth;

	var pongSocket: WebSocket;
	let canvas : HTMLCanvasElement;
	var scoring = 0;
	let isLoad : boolean = false;

	onMount(() => { (async () => {
		auth.subscribe((value : AuthState) =>{
            state = value;
        });

		isLoad = true;

		var skins
		let accessToken = await getAccessToken();
		if (accessToken == null)
			return ;
		const response = await fetch('/api/pong/skins/' + localStorage.getItem('game_id'), {
		method: 'GET',
		headers: { 'Authorization': `Bearer ${accessToken}` },
		});
		const data = await response.json();
		if (response.ok)
		{
			skins = data
		}

		var bind = {up: 90, down: 83, left:81, right:68, charge:32}

		const resp = await fetch('/api/pong/settings/' + state.user?.id + '/', {
		method: 'GET',
		headers: {'Authorization': `Bearer ${accessToken}`},
		});
		const dat = await resp.json();
		if (resp.ok)
		{
			bind = dat.settings
		}
		
		var canvasSize = {width: window.innerWidth * 0.7,  height: window.innerWidth * 0.7 / 16 * 9}
		var winner = 0



		const scene = new THREE.Scene();
		var end = 0
		

		var in_game = 0
		var startend = 0



		//var bind2 = {up: 38, down: 40, left:37, right:39, charge:96}
		var limit = {px: 0, py:8, nx:-18, ny:-8}
		var limit2 = {px: 18, py:8, nx: 0, ny:-8}
		var scores = [0, 0];
		var bots : Bot[];
		bots = []
		var id = 0;
		var fireworks: Firework [];
		fireworks = []
		var ui = document.getElementById("ui");
		var versus = document.getElementById("versus")
		var score1 = document.getElementById("player1")
		var score2 = document.getElementById("player2")
		var name1 = document.getElementById("player1_name")
		var name2 = document.getElementById("player2_name")
		var vs_name1 = document.getElementById("vs_name1")
		var vs_name2 = document.getElementById("vs_name2")



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


		const g = await loader.loadAsync('/assets/skins/vazy.glb');

		let i = 0;
		g.scene.scale.set(0.5, 0.5, 0.5);
		while (i < 4)
		{
			bots.push(new Bot(g.scene, collisions));
			scene.add(bots[i].mesh);
			i ++;
		}

		
		const gltf = await loader.loadAsync('/assets/skins/' + skins["player1"]["skin"]);


		gltf.scene.position.set(-10, 0, -1.5);
		gltf.scene.scale.set(0.5, 0.5, 0.5);
		gltf.scene.rotation.y = Math.PI / 2;
		gltf.scene.rotation.x = Math.PI / 2;

		var play = new Player(gltf, bind, limit, 0.15, 1);
		scene.add(play.mesh);




		const gl = await loader.loadAsync('/assets/skins/' + skins["player2"]["skin"]);

		gl.scene.position.set(10, 0, -1.5);
		gl.scene.scale.set(0.5, 0.5, 0.5);
		gl.scene.rotation.y = Math.PI * 3 / 2;
		gl.scene.rotation.x = Math.PI / 2;

		var er = new Player(gl, bind, limit2, 0.15, -1);
		scene.add(er.mesh);

		name1!.textContent = skins["player1"]["username"]
		name2!.textContent = skins["player2"]["username"]
		vs_name1!.textContent = skins["player1"]["username"]
		vs_name2!.textContent = skins["player2"]["username"]


		const lig = new THREE.DirectionalLight( 0xffffff, 1 );
		lig.position.set( 78, -2.5, 12.3 );
		scene.add( lig );

		const lg = new THREE.DirectionalLight( 0xffffff, 1);
		lg.position.set( -78, -2.5, 12.3 );
		scene.add( lg );




	
		const bouee = await loader.loadAsync('/assets/maps/pong/bouee.glb');
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
		dl.position.set( 0, 0, 30);
		scene.add( dl );

		const renderer = new THREE.WebGLRenderer({canvas, antialias: false});
		renderer.setSize( canvasSize.width, canvasSize.height);
        ui!.style.width = canvasSize.width + "px";
        ui!.style.height = canvasSize.height + "px";
        ui!.style.top = renderer.domElement.getBoundingClientRect().top + "px"
        ui!.style.left = renderer.domElement.getBoundingClientRect().left + "px"
		score1!.style.fontSize = canvasSize.height / 10 + "px"
		score2!.style.fontSize = canvasSize.height / 10 + "px"
		name1!.style.fontSize = canvasSize.height / 15 + "px"
		name2!.style.fontSize = canvasSize.height / 15 + "px"
		vs_name1!.style.fontSize = canvasSize.height / 15 + "px"
		vs_name2!.style.fontSize = canvasSize.height / 15 + "px"
		ui!.style.display = 'block'
		renderer.shadowMap.enabled = true;
		document.body.appendChild( renderer.domElement );

		
		const text = new THREE.TextureLoader().load('/assets/ui/pong/pp.jpg')
		text.colorSpace = "srgb";
		scene.background = text
		

		var xSpeed = 0.15;
		var ySpeed = 0.15;


		var ballspeed = 0.2;


		//#region CommandHandler

		document.addEventListener("keydown", onDocumentKeyDown, false);
		document.addEventListener("keyup", onDocumentKeyUp, false);

		const gamepads : { [id: number]: Gamepad} = {}

		function gamepadHandler(event : GamepadEvent, connected : boolean) {
			const gamepad = event.gamepad;

			if (connected) {
				gamepads[gamepad.index] = gamepad;
			} else {
				delete gamepads[gamepad.index];
			}
		}

		function handlebuttons(buttons : Gamepad["buttons"])
		{
			if (id == 1)
			{
				if (buttons[0].value > 0)
					play.controller.charge = 1;
				if (buttons[0].value == 0)
					play.controller.charge = 0;
			}
			if (id == 2)
			{
				if (buttons[0].value > 0)
					er.controller.charge = 1;
				if (buttons[0].value == 0)
					er.controller.charge = 0;
			}
		}

		var xSpeed = 0.15, ySpeed = 0.15;

		function handlesticks(axes : Gamepad["axes"])
		{
			if (id == 1)
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
			if (id == 2)
			{
				if (axes[0] < -0.2)
					er.controller.xn = axes[0] * xSpeed;
				else
					er.controller.xn = 0;
				if (axes[0] > 0.2)
					er.controller.xp = axes[0] * xSpeed;
				else
					er.controller.xp = 0;

				if (axes[1] < -0.2)
					er.controller.yn = -axes[1] * ySpeed;
				else
					er.controller.yn = 0;
				if (axes[1] > 0.2)
					er.controller.yp = -axes[1] * ySpeed;
				else
					er.controller.yp = 0;
			}
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
			ui!.style.width = canvasSize.width + "px";
			ui!.style.height = canvasSize.height + "px";
			ui!.style.top = renderer.domElement.getBoundingClientRect().top + "px"
			ui!.style.left = renderer.domElement.getBoundingClientRect().left + "px"
			score1!.style.fontSize = canvasSize.height / 10 + "px"
			score2!.style.fontSize = canvasSize.height / 10 + "px"
			name1!.style.fontSize = canvasSize.height / 15 + "px"
			name2!.style.fontSize = canvasSize.height / 15 + "px"
			vs_name1!.style.fontSize = canvasSize.height / 15 + "px"
			vs_name2!.style.fontSize = canvasSize.height / 15 + "px"
		}

		function onDocumentKeyDown(event : KeyboardEvent) {
			var keyCode = event.which;
			play.keydown(keyCode)
			er.keydown(keyCode)
		};

		function onDocumentKeyUp(event : KeyboardEvent) {
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
		const cam = new THREE.PerspectiveCamera( 50, 16 / 9, 0.1, 1000 );
		cam.position.set(0, -3.5, 82.3);
		cam.rotation.x = 1.26109338225244


		var frames = 0
		let url = '/ws/pong/pong/' + localStorage.getItem('room_name') + '/?token=' + accessToken;
		pongSocket = new WebSocket(url)

		pongSocket.onmessage = function(e) {
	
			let data = JSON.parse(e.data)
			if (data.event == 'Connected')
			{
				id = data.id
				pongSocket.send(JSON.stringify({
					'event':'ready',
					'id':id,
				}))
				play.mesh.position.set(-1.5, 0, 80)
				er.mesh.position.set(1.5, 0, 80)
				er.mesh.rotation.y += 0.25
				play.mesh.rotation.y -= 0.25
				play.mesh.translateZ(-10)
				er.mesh.translateZ(-10)
				er.controllanims.xp = 0.15
				play.controllanims.xp = -0.15
			}
			else if (data.event == 'ready')
			{
				pongSocket.send(JSON.stringify({
						'event':'ready',
						'id':id,
					}))
			}
			else if (data.event == 'start_game')
			{
				cam.position.set(0, 0, 20);
				cam.rotation.x = 0
				cam.fov = 70
				cam.updateProjectionMatrix ();
				play.mesh.rotation.y += 0.25
				er.mesh.rotation.y -= 0.25
				scene.background = null
				score1!.style.display = 'block'
				score2!.style.display = 'block'
				name1!.style.display = 'block'
				name2!.style.display = 'block'
				versus!.style.display = 'none'
				renderer.setClearColor( new THREE.Color(0xAAAAFF ) );
				er.controllanims.xp = 0
				play.controllanims.xp = 0
				in_game = 1 
			}
			else if (data.event == 'endMatch')
			{
				let copyBind = JSON.parse(JSON.stringify(bind))
				
				end = 1
				winner = data.id
				if (winner == 1)
				{
					bind["up"] = copyBind["right"]
					bind["left"] = copyBind["up"]
					bind["down"] = copyBind["left"]
					bind["right"] = copyBind["down"]
				}
				else
				{
					bind["up"] = copyBind["left"]
					bind["left"] = copyBind["down"]
					bind["down"] = copyBind["right"]
					bind["right"] = copyBind["up"]
				}
			}
			else if (data.event == 'frame')
			{
				play.mesh.position.set(data.player1[0], data.player1[1], -1.5)
				er.mesh.position.set(data.player2[0], data.player2[1], -1.5)
				if (data.player1[2] != scores[0])
				{
					scores[0] = data.player1[2]
					score1!.textContent = scores[0].toString()
				}
				if (data.player2[2] != scores[1])
				{
					scores[1] = data.player2[2]
					score2!.textContent = scores[1].toString()
				}
				play.controllanims = data.player1[3]
				er.controllanims = data.player2[3]
				sphere.position.set(data.ball, data.bally, sphere.position.z);
				scoring = data.scoring
				if (id == 1)
				{
					pongSocket.send(JSON.stringify({
						'event':'frame',
						'player1':play.controller,
					}))
				}
				if (id == 2)
				{
					pongSocket.send(JSON.stringify({
						'event':'frame',
						'player2':er.controller,
					}))
				}
			}
		}

		pongSocket.onclose = function(e) {
			if (e.code != 1000)
				goto('/');
		}


		function animate() {
			if (isLoad)
				requestAnimationFrame( animate );
			if (in_game == 1)
			{
				const dt = clock.getDelta();
				plain.material.uniforms.time.value = t * 70;
				t += dt;
				if (gamepads[0])
				{
					let pad = navigator.getGamepads()[0]
					if (pad)
						gamepads[0] = pad
					handlebuttons(gamepads[0].buttons)
					handlesticks(gamepads[0].axes)
				}
				play.update()
				er.update()

				bots.forEach(element => {
					element.update();
					element.scoring = scoring;
				});
				if (end == 1)
				{
					cam.rotation.x = THREE.MathUtils.lerp(cam.rotation.x, Math.PI / 2, 0.1)
					cam.rotation.y = THREE.MathUtils.lerp(cam.rotation.y, -Math.pow(-1, winner) * Math.PI / 2, 0.1)
					cam.position.z = THREE.MathUtils.lerp(cam.position.z, 2, 0.1)
					startend += dt
					if (startend >= 20)
					{
						pongSocket.close()
						goto('/');
					}
					if( THREE.MathUtils.randInt( 1, 50 ) === 10)
    				{
    				    fireworks.push( new Firework( scene, 20 * Math.pow(-1, winner) ) ); 
    				}
    				for( var i = 0; i < fireworks.length; i++ )
    				{
    				    if( fireworks[ i ].done )  
    				    {
    				        fireworks.splice( i, 1 ); 
    				        continue; 
    				    }
    				    fireworks[ i ].update(dt);
    				}
				}
			}
			else
			{
				if (play.mesh.position.x < -1.5)
					play.mesh.translateZ(0.1)
				if (er.mesh.position.x > 1.5)
				 	er.mesh.translateZ(0.1)
				play.update()
				er.update()
			}
			renderer.render( scene, cam );
		}
		animate();
	})();
	});

	onDestroy(() => {
		isLoad = false;
		if (pongSocket)
			pongSocket.close();
	})
</script>

<style>
	/*@import url('https://fonts.googleapis.com/css2?family=Lilita+One&display=swap');*/
	@import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');
    #ui {
		display: none;
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

	#versus {
		pointer-events: none;
		display:flex;
		position: absolute;
		width: 100%;
		height: 100%;
	}

	#player1, #player2, #player1_name, #player2_name {
		display: none;
	}
	
	#vs_name1, #vs_name2 {
		bottom: 3%;
		position: absolute;
		text-shadow: none;
	}

	#vs_name1 {
		transform: translate(-50%);
		left: 19%
	}

	#vs_name2 {
		transform: translate(50%);
		right: 19%
	}

	#vs {
		position: absolute;
		top: 49%;
		left:50.7%
	}

	#vs >img {
		position: relative;
		height: auto;
		width: 68.7%;
		transform: translate(-50%, -50%);
	}

</style>

<div id="ui">
	<div id="score">
		<span class="text" id="player1_name"></span>
		<span class="text" id="player1">0</span>
		<span class="text" id="player2">0</span>
		<span class="text" id="player2_name"></span>
	</div>
	<div id="versus">
		<div id="vs">
			<img alt="versus_logo" src="/assets/ui/pong/vzs.png"/>
		</div>
		<span class="text" id="vs_name1"></span>
		<span class="text" id="vs_name2"></span>
	</div>
</div>


<canvas bind:this={canvas} class='d-flex flex-column game'></canvas>

