<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import * as THREE from 'three';
	import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
	import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer'
	import { RenderPixelatedPass } from  'three/examples/jsm/postprocessing/RenderPixelatedPass';
	import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
	import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
	import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass'
	import { Player } from "./player.js";
	import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
	import {CrtShader} from "./crtShader.js";
	import { auth, fetchUser } from '$lib/stores/auth';
	import type { AuthState } from '$lib/stores/auth';
	import { goto } from '$app/navigation';

	var pongSocket: WebSocket;
	let canvas;
	var scoring = 0;
	let state: AuthState;
	$: $auth, state = $auth;

	onMount(() => { (async () => {
		await fetchUser()
		auth.subscribe((value : AuthState) =>{
            state = value;
        });
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera( 70, 16 / 9, 0.1, 1000 );
		scene.background = new THREE.Color(0x000000);


		var skins
		const response = await fetch('/api/pong/skins/' + localStorage.getItem('game_id'), {
		method: 'GET',
		headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
		});
		const data = await response.json();
		if (response.ok)
		{
			skins = data
		}


		
		var bind = {up: 90, down: 83, left:81, right:68, charge:32}
		//var bind2 = {up: 38, down: 40, left:37, right:39, charge:96}
		var limit = {px: 0, py:8, nx:-18, ny:-8}
		var limit2 = {px: 18, py:8, nx: 0, ny:-8}
		var scores = [0, 0];
		var endtext;
		var startend = 0;
		var id = 0;
		var ui = document.getElementById("ui");
		var score1 = document.getElementById("player1")
		var score2 = document.getElementById("player2")
		var name1 = document.getElementById("player1_name")
		var name2 = document.getElementById("player2_name")
		var canvasSize = {width: window.innerWidth * 0.7,  height: window.innerWidth * 0.7 / 16 * 9}


		name1.textContent = skins["player1"]["username"]
		name2.textContent = skins["player2"]["username"]

		//#region LoadModel

		var end = 0
		const loader = new GLTFLoader()

		const WinMesh = await loader.loadAsync('src/routes/(private)/pong_retro/public/win.glb');
		WinMesh.scene.rotation.x = Math.PI / 2
		WinMesh.scene.position.z = 15
		WinMesh.scene.position.x = -2.25
		WinMesh.scene.scale.y = 0.1
		const winMat = new THREE.MeshStandardMaterial( { color: 0x0000FF } ); 
		WinMesh.scene.traverse(function(node) {
            if (node.isMesh)
				node.material = winMat;
                node.layers.toggle(1);
        })

		const LoseMesh = await loader.loadAsync('src/routes/(private)/pong_retro/public/lose.glb');
		LoseMesh.scene.rotation.x = Math.PI / 2
		LoseMesh.scene.position.z = 15
		LoseMesh.scene.position.x = -2.25
		LoseMesh.scene.scale.y = 0.1
		const loseMat = new THREE.MeshStandardMaterial( { color: 0xFF0000 } ); 
		LoseMesh.scene.traverse(function(node) {
            if (node.isMesh)
                node.layers.toggle(1);
				node.material = loseMat;
        })



		const gltf = await loader.loadAsync('src/routes/(private)/pong_retro/public/blank.glb');


		gltf.scene.position.set(-17, 0, -1.5);
		gltf.scene.scale.set(0.5, 0.5, 0.5);
		gltf.scene.rotation.y = Math.PI / 2;
		gltf.scene.rotation.x = Math.PI / 2;

		var play = new Player(gltf, bind, limit, 0.15, 1);
		scene.add(play.mesh);




		const gl = await loader.loadAsync('src/routes/(private)/pong_retro/public/blank.glb');

		gl.scene.position.set(17, 0, -1.5);
		gl.scene.scale.set(0.5, 0.5, 0.5);
		gl.scene.rotation.y = Math.PI * 3 / 2;
		gl.scene.rotation.x = Math.PI / 2;

		var er = new Player(gl, bind, limit2, 0.15, -1);
		scene.add(er.mesh);

		er.mesh.traverse(function(node) {
            if (node.isMesh)
                node.layers.toggle(1);
        })
		play.mesh.traverse(function(node) {
            if (node.isMesh)
                node.layers.toggle(1);
        })

		const win = await loader.loadAsync('src/routes/(private)/pong_retro/public/win.glb');
		

		//#endregion


		//#region CreateMesh

		const geo = new THREE.SphereGeometry( 0.8, 32, 16); 
		const mat = new THREE.MeshStandardMaterial( { color: 0xFF0000 } ); 
		const sphere = new THREE.Mesh( geo, mat );
		sphere.layers.toggle(1)
		scene.add( sphere );

		let spherebb = new THREE.Sphere(sphere.position, 1);

		const textur = new THREE.TextureLoader().load( "src/routes/(private)/pong_retro/public/suhd.png" );
		textur.wrapS = THREE.RepeatWrapping;

		textur.wrapT = THREE.RepeatWrapping;

		const plain = new THREE.Mesh(new THREE.PlaneGeometry(52, 30), new THREE.MeshStandardMaterial( { map :textur }));
		//plain.layers.toggle(1)


		plain.position.set(0, 0, -4.8);
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
		renderer.setSize( canvasSize.width, canvasSize.height);
        ui.style.width = canvasSize.width + "px";
        ui.style.height = canvasSize.height + "px";
        ui.style.top = renderer.domElement.getBoundingClientRect().top + "px"
        ui.style.left = renderer.domElement.getBoundingClientRect().left + "px"
		score1.style.fontSize = canvasSize.height / 10 + "px"
		score2.style.fontSize = canvasSize.height / 10 + "px"
		name1.style.fontSize = canvasSize.height / 15 + "px"
		name2.style.fontSize = canvasSize.height / 15 + "px"
		renderer.shadowMap.enabled = true;
		document.body.appendChild( renderer.domElement );

		camera.position.z = 18;

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
			canvasSize.width = window.innerWidth * 0.7
			canvasSize.height = window.innerWidth * 0.7 / 16 * 9
			renderer.setSize( canvasSize.width, canvasSize.height);
			composer.setSize( canvasSize.width, canvasSize.height );
			finalComposer.setSize( canvasSize.width, canvasSize.height );
            ui.style.width = canvasSize.width + "px";
            ui.style.height = canvasSize.height + "px";
            ui.style.top = renderer.domElement.getBoundingClientRect().top + "px"
            ui.style.left = renderer.domElement.getBoundingClientRect().left + "px"
			score1.style.fontSize = canvasSize.height / 10 + "px"
			score2.style.fontSize = canvasSize.height / 10 + "px"
			name1.style.fontSize = canvasSize.height / 15 + "px"
			name2.style.fontSize = canvasSize.height / 15 + "px"
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

		let url = '/ws/pong/pong_retro/' + localStorage.getItem('room_name') + '/?token=' + localStorage.getItem('access_token');
		pongSocket = new WebSocket(url)

		pongSocket.onmessage = function(e) {
	
			let data = JSON.parse(e.data)
			if (data.event == 'Connected')
			{
				id = data.id
				if (id == 1)
				{
				pongSocket.send(JSON.stringify({
					'event':'frame',
					'player1':play.controller,
					'game':"pong_retro"
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
			else if (data.event == 'endMatch')
			{
				scene.remove(play.mesh)
				scene.remove(er.mesh)
				end = 1;
				if (data.id == id)
					endtext = WinMesh.scene;
				else
					endtext = LoseMesh.scene;
				scene.add(endtext)
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
				if (id == 1 && end == 0)
				{
					pongSocket.send(JSON.stringify({
						'event':'frame',
						'player1':play.controller,
					}))
				}
				if (id == 2 && end == 0)
				{
					pongSocket.send(JSON.stringify({
						'event':'frame',
						'player2':er.controller,
					}))
				}
			}
		}

		pongSocket.onclose = function(e) {
			goto('/');
		}

		//#endregion

		const renderScene = new RenderPass( scene, camera )

		const composer = new EffectComposer( renderer );
		composer.addPass( renderScene );



		const params = {
			threshold: 0,
			strength: 0.4,
			radius: 1,
			exposure: 1
		};

		const bloomPass = new UnrealBloomPass( new THREE.Vector2( canvasSize.width, canvasSize.height ), 1.5, 0.4, 0.85 );
		bloomPass.threshold = params.threshold;
		bloomPass.strength = params.strength;
		bloomPass.radius = params.radius;

		composer.addPass(bloomPass)

		composer.renderToScreen = false;

		const mixPass = new ShaderPass(
			new THREE.ShaderMaterial( {
					uniforms: {
						baseTexture: { value: null },
						bloomTexture: { value: composer.renderTarget2.texture }
					},
					vertexShader:`
					varying vec2 vUv;

					void main() {
						vUv = uv;
						gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
					}`,
					fragmentShader:`
					uniform sampler2D baseTexture;
					uniform sampler2D bloomTexture;
					varying vec2 vUv;
						
					void main() {
						gl_FragColor = ( texture2D( baseTexture, vUv ) + vec4( 1.0 ) * texture2D( bloomTexture, vUv ) );
					}`,
					defines: {}
				} ), 'baseTexture'
			);

		const finalComposer = new EffectComposer( renderer );
		
		finalComposer.addPass( renderScene )
		finalComposer.addPass( mixPass )
		const crt = new ShaderPass( CrtShader )
		finalComposer.addPass(crt)

		const output = new OutputPass()
		finalComposer.addPass(output)

		const BLOOM_SCENE = 1;
		const bloomLayer = new THREE.Layers();
		bloomLayer.set(BLOOM_SCENE);
		const darkMaterial = new THREE.MeshBasicMaterial({color: 0x000000})
		const materials = {}

		function nonBloomed(obj) {
			if(obj.isMesh && bloomLayer.test(obj.layers) == false) 
			{
				materials[obj.uuid] = obj.material;
				obj.material = darkMaterial;
			}
		}

		function restoreMaterial(obj) {
			if (materials[obj.uuid])
			{
				obj.material = materials[obj.uuid];
				delete materials[obj.uuid];
			}
		}





		// var renderPixelatedPass = new RenderPixelatedPass(3.5, scene, camera );
		// composer.addPass( renderPixelatedPass );

		function animate() {
			requestAnimationFrame( animate );
			const dt = clock.getDelta();
			t += dt;
			if (gamepads[0])
			{
				gamepads[0] = navigator.getGamepads()[0]
				handlebuttons(gamepads[0].buttons)
				handlesticks(gamepads[0].axes)
			}
			if (end == 1)
			{
				startend += dt
				if (Math.floor(startend % 2) == 1)
					scene.remove(endtext)
				else
					scene.add(endtext)
				if (startend >= 5)
					pongSocket.close()
			}
			scene.traverse(nonBloomed)
			composer.render();
			scene.traverse(restoreMaterial)
			finalComposer.render()
			play.update(dt)
			er.update(dt)
			
		}
		animate();
	})();
	});

	onDestroy(() => {
		if (pongSocket)
			pongSocket.close()
	})
</script>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Silkscreen:wght@400;700&display=swap');
	/*@import url('https://fonts.googleapis.com/css2?family=Tiny5&display=swap');*/
    #ui {
        position: absolute;
		width: 10px;
		height: 10px;

    }

	.game {
		border-radius: 3% !important;
        margin: auto !important;
    }

	#score {
		position: absolute;
		width: 100%;
		height: 100%;
		display:flex;
		justify-content: space-evenly;
	}

	.text {
		font-family: "Silkscreen", sans-serif;
		/*font-family: "Tiny5", sans-serif;*/
  		/* font-weight: 400; */
		margin-top: 3%;
  		font-style: normal;
		color:white;
		font-size: 70px;
	}




</style>

<div id="ui">
	<div id="score">
		<span class="text" id="player1_name"></span>
		<span class="text" id="player1">0</span>
		<span class="text" id="player2">0</span>
		<span class="text" id="player2_name"></span>
	</div>
</div>


<canvas bind:this={canvas} class="d-flex flex-column game"></canvas>