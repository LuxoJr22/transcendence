<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import * as THREE from 'three';
	import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
	import { Player } from "./player.js";
	import { Bot } from "./bot.js";
	import { shade } from "./watershader";
	import { Firework } from './firework.js';

	var pongSocket: WebSocket;
	let canvas;
	var scoring = 0;

	onMount(() => { (async () => {

		var skins
		const response = await fetch('api/pong/skins/' + localStorage.getItem('game_id'), {
		method: 'GET',
		headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
		});
		const data = await response.json();
		if (response.ok)
		{
			skins = data
		}

		var canvasSize = {width: window.innerWidth * 0.7,  height: window.innerWidth * 0.7 / 16 * 9}
		var winner = 0



		const scene = new THREE.Scene();
		const cam = new THREE.PerspectiveCamera( 70, 16 / 9, 0.1, 1000 );
		var end = 0
		

		var in_game = 0
		var startend = 0


		var bind = {up: 90, down: 83, left:81, right:68, charge:32}
		//var bind2 = {up: 38, down: 40, left:37, right:39, charge:96}
		var limit = {px: 0, py:8, nx:-18, ny:-8}
		var limit2 = {px: 18, py:8, nx: 0, ny:-8}
		var scores = [0, 0];
		var bots = [];
		var id = 0;
		var fireworks = [];
		var ui = document.getElementById("ui");
		var score = document.getElementById("score");
		var versus = document.getElementById("versus")
		var score1 = document.getElementById("player1")
		var score2 = document.getElementById("player2")

		score1.style.display = 'none'
		score2.style.display = 'none'
		
		var endscoring = 0;

		const views = [
			{
				left: 0,
				bottom: 0,
				width: 0.5,
				height: 1.0,
				eye: [ -78, -2.5, 12.3 ],
				rotation : [1.26109338225244, 0.6510985849711179, 0.19156132032912654],
				background: new THREE.Color().setRGB( 0.3, 0.3, 0.9, THREE.SRGBColorSpace ),
				camera: null,
			},
			{
				left: 0.5,
				bottom: 0,
				width: 0.5,
				height: 1.0,
				eye: [ 78, -2.5, 12.3 ],
				rotation : [1.26109338225244, -0.6510985849711179, -0.19156132032912654],
				background: new THREE.Color().setRGB( 0.9, 0.2, 0.2, THREE.SRGBColorSpace ),
				camera: null,
			}
		]

		for ( let i = 0; i < views.length; ++ i ) {

			const view = views[ i ];
			const camera = new THREE.PerspectiveCamera( 50, 16 / 9, 1, 1000 );
			camera.position.fromArray( view.eye );
			camera.up.fromArray( [0, 0, 1]);
			camera.rotation.fromArray( view.rotation)
			view.camera = camera;
		}



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

		
		const gltf = await loader.loadAsync('src/lib/assets/skins/' + skins["player1"]["skin"]);


		gltf.scene.position.set(-10, 0, -1.5);
		gltf.scene.scale.set(0.5, 0.5, 0.5);
		gltf.scene.rotation.y = Math.PI / 2;
		gltf.scene.rotation.x = Math.PI / 2;

		var play = new Player(gltf, bind, limit, 0.15, 1);
		scene.add(play.mesh);




		const gl = await loader.loadAsync('src/lib/assets/skins/' + skins["player2"]["skin"]);

		gl.scene.position.set(10, 0, -1.5);
		gl.scene.scale.set(0.5, 0.5, 0.5);
		gl.scene.rotation.y = Math.PI * 3 / 2;
		gl.scene.rotation.x = Math.PI / 2;

		var er = new Player(gl, bind, limit2, 0.15, -1);
		scene.add(er.mesh);



		const lig = new THREE.DirectionalLight( 0xffffff, 1 );
		lig.position.set( 78, -2.5, 12.3 );
		scene.add( lig );

		const lg = new THREE.DirectionalLight( 0xffffff, 1);
		lg.position.set( -78, -2.5, 12.3 );
		scene.add( lg );




	
		const bouee = await loader.loadAsync('src/routes/(private)/pong/public/bue.glb');
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
        ui.style.width = canvasSize.width + "px";
        ui.style.height = canvasSize.height + "px";
        ui.style.top = renderer.domElement.getBoundingClientRect().top + "px"
        ui.style.left = renderer.domElement.getBoundingClientRect().left + "px"
		score1.style.fontSize = canvasSize.height / 10 + "px"
		score2.style.fontSize = canvasSize.height / 10 + "px"
		renderer.shadowMap.enabled = true;
		document.body.appendChild( renderer.domElement );

		


		cam.position.z = 20;

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

		function handlesticks(axes)
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
			ui.style.width = canvasSize.width + "px";
			ui.style.height = canvasSize.height + "px";
			ui.style.top = renderer.domElement.getBoundingClientRect().top + "px"
			ui.style.left = renderer.domElement.getBoundingClientRect().left + "px"
			score1.style.fontSize = canvasSize.height / 10 + "px"
			score2.style.fontSize = canvasSize.height / 10 + "px"
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


		var frames = 0
		let url = '/ws/pong/pong/' + localStorage.getItem('room_name') + '/?token=' + localStorage.getItem('access_token');
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
				play.mesh.position.set(-80 ,0, 10)
				er.mesh.position.set(80, 0, 10)
				play.mesh.translateZ(-10)
				er.mesh.translateZ(-10)
				er.controllanims.xp = 0.15
				play.controllanims.xp = -0.15
			}
			else if (data.event == 'start_game')
			{
				score1.style.display = ''
				score2.style.display = ''
				versus.style.display = 'none'
				renderer.setScissorTest( false );
				renderer.setViewport(0, 0, window.innerWidth * 0.7, (window.innerWidth * 0.70) / 16 * 9)
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
			window.location.href = '/';
		}


		function animate() {
			requestAnimationFrame( animate );
			if (in_game == 1)
			{
				const dt = clock.getDelta();
				plain.material.uniforms.time.value = t * 70;
				t += dt;
				if (gamepads[0])
				{
					gamepads[0] = navigator.getGamepads()[0]
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
						pongSocket.close()
					if( THREE.MathUtils.randInt( 1, 50 ) === 10)
    				{
    				    fireworks.push( new Firework( scene, [20 * Math.pow(-1, winner)] ) ); 
    				}
    				// update fireworks 
    				for( var i = 0; i < fireworks.length; i++ )
    				{
    				    if( fireworks[ i ].done ) // cleanup 
    				    {
    				        fireworks.splice( i, 1 ); 
    				        continue; 
    				    }
    				    fireworks[ i ].update(dt);
    				}
				}
				renderer.render( scene, cam );
			}
			else
			{
				for ( let ii = 0; ii < views.length; ++ ii ) {

					const view = views[ ii ];
					const camera = view.camera;

					const left = Math.floor(window.innerWidth * 0.7 * view.left);
					const bottom = Math.floor((window.innerWidth * 0.70) / 16 * 9 * view.bottom);
					const width = Math.floor(window.innerWidth * 0.7 * view.width );
					const height = Math.floor((window.innerWidth * 0.70) / 16 * 9 *  view.height );


					renderer.setViewport( left, bottom, width, height );
					renderer.setScissor( left, bottom, width, height );
					renderer.setScissorTest( true );
					renderer.setClearColor( view.background );

					camera.aspect = width / height;
					camera.updateProjectionMatrix();

					renderer.render( scene, camera );
				}
				if (play.mesh.position.x < -80)
					play.mesh.translateZ(0.1)
				if (er.mesh.position.x > 80)
					er.mesh.translateZ(0.1)
				play.update()
				er.update()
			}
		}
		animate();
	})();
	});

	onDestroy(() => {
		if (pongSocket)
			pongSocket.close();
	})
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
		display: none;
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
		top: 45%;
		left: 50%;
	}

	#vs {
		position: relative;
	}

	#vs >img {
		position: relative;
		height: auto;
		width: 50%;
		transform: translate(-50%, -50%);
	}




</style>

<div id="ui">
	<div id="score">
		<span class="text" id="player1">0</span>
		<span class="text" id="player2">0</span>
	</div>
	<div id="versus">
		<div id="vs">
			<img src="src/routes/(private)/pong/public/vers.png"/>
		</div>
	</div>
</div>


<canvas bind:this={canvas} class='d-flex flex-column game'></canvas>

