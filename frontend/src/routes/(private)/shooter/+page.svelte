<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { GUI } from 'three/addons/libs/lil-gui.module.min.js';
    import * as THREE from 'three';
    import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
    import { Shooter } from "./shooter.js";
    import { Player } from "./player.js";
    import { flagshader } from "./flagshader.js";
    import { createmap } from "./map.js"
    import { SkeletonCollider } from "./skeletoncollider.js"
    import { VertexNormalsHelper } from 'three/addons/helpers/VertexNormalsHelper.js';
    import { auth } from '$lib/stores/auth';
	import type { AuthState } from '$lib/stores/auth';

	let state: AuthState;
	$: $auth, state = $auth;
    var chatSocket: WebSocket;

    let canvas;

    onMount(() => { (async () => {
        auth.subscribe((value : AuthState) =>{
            state = value;
        });
        var match_id

        const response = await fetch('api/shooter/create/', {
		method: 'POST',
		headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
		});
		const data = await response.json();
		if (response.ok)
		{
			match_id = data.match
		}

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera( 70, 16 / 9, 0.1, 1000 );
        
        var pointerLockActivated = 0

        let t = 0;
        const clock = new THREE.Clock();
        var reload = 0;
        var boostreload = 0

        // var canvas = document.getElementById("canvas")
        var el = document.getElementById("blocker");
        var ui = document.getElementById("ui");
        var circle = document.getElementById("circular");
        var ficon = document.getElementById("flagicon");
        var scoreboard = document.getElementById("scoreboard")
        var timer = document.getElementById("timer")
        var table_body = document.getElementById("mytbody")

        var score_cells = []

        var players = []


        scene.background = new THREE.Color(0x54A0E4);


        
        var bind = {up: 90, down: 83, left:81, right:68, jump:32}

        const resp = await fetch('api/shooter/settings/' + state.user?.id, {
		method: 'GET',
		headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` },
		});
		const dat = await resp.json();
		if (resp.ok)
		{
			bind = dat.settings
		}


        var id = 0
        
        createmap(scene);


        const sh = new THREE.Mesh(new THREE.TorusGeometry(1.5, 0.1, 20), flagshader)
        sh.rotation.x = Math.PI / 2;
        sh.position.set(0, 6, -5)
        scene.add(sh)

        const tor = new THREE.Mesh(new THREE.TorusGeometry(1.5, 0.1, 20), flagshader.clone())
        tor.rotation.x = Math.PI / 2;
        tor.position.set(0, 6, -5)
        scene.add(tor)

        const toru = new THREE.Mesh(new THREE.TorusGeometry(1.5, 0.1, 20), flagshader.clone())
        toru.rotation.x = Math.PI / 2;
        toru.position.set(0, 6, -5)
        scene.add(toru)


        const loader = new GLTFLoader()

        const flag = await loader.loadAsync('src/routes/(private)/shooter/public/f.glb');
        flag.scene.name = 'flag'
        flag.scene.position.set(0, 5, -5);
        

        const mount = await loader.loadAsync('src/routes/(private)/shooter/public/mountain.glb');
        //scene.add(mount.scene);

        
        //mount.scene.children[0].children[0].geometry.applyMatrix4(new THREE.Matrix4().makeScale(20, 20, 20));
        //mount.scene.children[0].children[1].geometry.applyMatrix4(new THREE.Matrix4().makeScale(20, 20, 20));


        var play = new Shooter(bind, 0.15, camera, scene);
        
            //scene.add(play.mesh);

        el.addEventListener('click', function () {
            let now = performance.now()
            if (pointerLockActivated && now - pointerLockActivated < 1100)
                return
            el.style.display = "none";
            play.cam.lock();
            
            
        });


        play.cam.addEventListener( 'unlock', function () {
            pointerLockActivated = performance.now()
            el.style.display = '';
        } );

        scene.add(play.cam.getObject());



        //#endregion



        const amblight = new THREE.AmbientLight( 0xffffff, 0.7 );
		scene.add( amblight );

        const dl = new THREE.DirectionalLight( 0xffffff, 1.0 );
        
        dl.position.set( 0, 100, 0 );
        dl.target.position.set(0, 0, 0)
        dl.castShadow = true;
        scene.add( dl );
        scene.add( dl.target)
        var size = 50;
        dl.shadow.camera.top = size;
        dl.shadow.camera.bottom = -size;
        dl.shadow.camera.left = size;
        dl.shadow.camera.right = -size;

        const renderer = new THREE.WebGLRenderer({canvas, antialias: false});
        var canvasSize = {width: (window.innerHeight) * 16 / 9,  height: (window.innerHeight)}
        if (canvasSize.width > window.innerWidth)
        {
            canvasSize.width =  (window.innerWidth)
		    canvasSize.height =  (window.innerWidth) * 9 / 16
        }
        renderer.setSize( canvasSize.width, canvasSize.height);
        ui.style.width = canvasSize.width + "px";
        ui.style.height = canvasSize.height + "px";
        ui.style.top = renderer.domElement.getBoundingClientRect().top + "px"
        ui.style.left = renderer.domElement.getBoundingClientRect().left + "px"
        timer.style.fontSize = canvasSize.height / 10 + "px"
		renderer.shadowMap.enabled = true;
        document.body.appendChild( renderer.domElement );


        var xSpeed = 0.15;
        var ySpeed = 0.15;

        //#region CommandHandler

        document.addEventListener("keydown", onDocumentKeyDown, false);
        document.addEventListener("keyup", onDocumentKeyUp, false);
        document.addEventListener("mousedown", onMouse, false);

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
                play.controller.jump = 1;
            if (buttons[0].value == 0)
                play.controller.jump = 0;
            if (buttons[7].value > 0.5)
                shoot()
            if (buttons[6].value > 0.5)
                jumpBoost()
        }

        var xSpeed = 0.15, ySpeed = 0.15;

        camera.rotation.order = "YXZ"


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

            if (axes[2] < -0.2)
                play.cam.getObject().rotation.y -= axes[2] * xSpeed / 2;
            if (axes[2] > 0.2)
                play.cam.getObject().rotation.y -= axes[2] * xSpeed / 2;

            if (axes[3] < -0.2 && play.cam.getObject().rotation.x < 1.5)
            {
                play.cam.getObject().rotation.x -= axes[3] * xSpeed / 2;
            }
            if (axes[3] > 0.2 && play.cam.getObject().rotation.x > -1.5)
            {
                play.cam.getObject().rotation.x -= axes[3] * xSpeed / 2;
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
			canvasSize.width =  (window.innerHeight) * 16 / 9
			canvasSize.height =  (window.innerHeight)
            if (canvasSize.width > window.innerWidth)
            {
                canvasSize.width =  (window.innerWidth)
			    canvasSize.height =  (window.innerWidth) * 9 / 16
            }

            renderer.setSize( canvasSize.width, canvasSize.height);
            ui.style.width = canvasSize.width + "px";
            ui.style.height = canvasSize.height + "px";
            ui.style.top = renderer.domElement.getBoundingClientRect().top + "px"
            ui.style.left = renderer.domElement.getBoundingClientRect().left + "px"
            timer.style.fontSize = canvasSize.height / 10 + "px"

            
        }

        
        function onMouse(event) {
            if (event.which == 1)
            {
                shoot()
            }
            if (event.which == 3)
            {
                jumpBoost()
            }
        }

        function shoot() {
            if (reload == 0)
            {
                var intersects = play.raycaster.intersectObjects( scene.children );
                reload = 360;
                let i = 0
                if (intersects[i] && intersects[ i ].object == play.bb)
                    i ++;
                if (intersects[i] && intersects[ i ].object != play.sphere)
                {
                    play.sphere.position.set(intersects[i].point.x, intersects[i].point.y ,intersects[i].point.z );
                    if (play.target.includes(intersects[i].object))
                    {
                        chatSocket.send(JSON.stringify({
                        'event':'hit',
                        'id':id,
                        'target':intersects[i].object.userData.id
                        }))
                    }
                }
            }
        }

        function jumpBoost() {
            if (boostreload == 0)
            {
                boostreload = 50
                var intersects = play.raycaster.intersectObjects( scene.children );
                let i = 0
                if ((intersects[i] && intersects[ i ].object == play.bb) || (intersects[i] && intersects[ i ].object.type == "Line"))
                    i ++;
                if (intersects[i] && intersects[ i ].object != play.sphere)
                {
                    play.sphere.position.set(intersects[i].point.x, intersects[i].point.y ,intersects[i].point.z );
                    if (play.bbox.intersectsSphere(play.spherebb))
                    {
                        if (play.velocity.y < 0 && play.cam.getObject().position.y - intersects[i].point.y > 0)
                            play.velocity.y = 0;
                        if (intersects[i].distance < 0.5)
                            intersects[i].distance = 0.5;
                        play.force.y += (play.cam.getObject().position.y - intersects[i].point.y) * 50 / intersects[ i ].distance;
                        play.force.x += (play.cam.getObject().position.x - intersects[i].point.x) * 50 / intersects[ i ].distance;
                        play.force.z += (play.cam.getObject().position.z - intersects[i].point.z) * 50 / intersects[ i ].distance;
                    }
                }
            }
        }

        async function createPlayer(play_id, skin) {
            const gl = await loader.loadAsync('src/lib/assets/skins/' + skin);
            gl.scene.position.set(10, 0, -1.5);
            gl.scene.scale.set(0.5, 0.5, 0.5);
            let pl = new Player(gl, 0.15, scene, play_id)
            play.target = play.target.concat(pl.target)
            players.push(pl);
        }

        let url = '/ws/shooter/shooter_' + match_id + '/?token=' + localStorage.getItem('access_token');
		chatSocket = new WebSocket(url)
        
		chatSocket.onmessage = function(e) {
	
			let data = JSON.parse(e.data)
			if (data.event == 'Connected' && id == 0)
			{
                id = data.id
                let i = 0;
                if (data.flag == 0)
                    scene.add(flag.scene)
                while (data.players[i])
                {
                    if (i != id - 1)
                        createPlayer(i, data.players[i].skin)
                    var row = table_body.insertRow()
                    var usercell = row.insertCell(0)
                    var scorecell = row.insertCell(1)

                    usercell.innerHTML = data.players[i].username
                    scorecell.innerHTML = Math.round(data.players[i].score)
                    score_cells.push(scorecell)
                    i ++;
                }
                camera.position.z = data.position.z;
                camera.position.y = data.position.y;
                camera.position.x = data.position.x;
                camera.rotation.x = data.rotation.x;
                camera.rotation.y = data.rotation.y;
                camera.rotation.z = data.rotation.z;

                chatSocket.send(JSON.stringify({
					'event':'frame',
					'player':[play.cam.getObject().position, play.direction],
                    'controller':play.controller,
                    'id':id
				}))
			}
            else if (data.event == 'Connected')
            {
                let i = 0
                while (players[i])
                {
                    players[i].target.forEach(el => {scene.remove(el)})
                    players[i].mesh.geometry = undefined
                    players[i].mesh.material = undefined
                    scene.remove(players[i].mesh)
                    if (players[i].id == data.id - 1)
                        players.splice(i, 1)
                    i ++
                }
                createPlayer(data.id - 1, data.players[data.id - 1].skin)

                var row = table_body.insertRow()
                var usercell = row.insertCell(0)
                var scorecell = row.insertCell(1)
                usercell.innerHTML = data.players[id].username
                scorecell.innerHTML = Math.round(data.players[id].score)
                score_cells.push(scorecell)
            }
            if (data.event == 'Flag_picked')
            {
                if (data.id == id)
                    ficon.style.display = "block";
                scene.remove(flag.scene);
            }
            if (data.event == 'Flag_dropped')
            {
                if (data.id == id)
                    ficon.style.display = "none";
                scene.add(flag.scene);
                scene.add(sh)
                scene.add(tor)
                scene.add(toru)
            }
            if (data.event == 'frame')
            {
                let i = 0
                timer_update(Math.floor(data.timer))
                while (players[i])
                {
                    let actid = players[i].id
                    if (players[i].id != id - 1)
                    {
                        
                        players[i].mesh.position.set(data.players[actid].position.x, data.players[actid].position.y - 2, data.players[actid].position.z)
                        if (data.players[actid].direction.y < 0)
                            players[i].mesh.rotation.y = Math.acos(data.players[actid].direction.x) + (Math.PI / 2)
                        else
                            players[i].mesh.rotation.y = -Math.acos(data.players[actid].direction.x) + (Math.PI / 2)
                        players[i].controller = data.players[actid].controller
                        
                    }
                    score_cells[actid].innerHTML = Math.round(data.players[actid].score)
                    i ++;
                }
                score_cells[id - 1].innerHTML = Math.round(data.players[id - 1].score)
				chatSocket.send(JSON.stringify({
					'event':'frame',
					'player':[play.cam.getObject().position, play.direc],
                    'controller':play.controller,
                    'id':id
				}))
            }
            if (data.event == "hit")
            {
                play.cam.getObject().position.x = data.position.x
                play.cam.getObject().position.y = data.position.y
                play.cam.getObject().position.z = data.position.z
                play.cam.getObject().rotation.x = data.rotation.x
                play.cam.getObject().rotation.y = data.rotation.y
                play.cam.getObject().rotation.z = data.rotation.z
            }
            if (data.event == "Quit")
                window.location.href = '/';
		}

        function timer_update(totalSeconds)
        {
            if (totalSeconds < 0)            
                totalSeconds = 0
            let seconds = totalSeconds % 60;
            let secondsTens = Math.floor(seconds / 10);
            let secondsOnes = seconds % 10;
            let minutes = Math.floor(totalSeconds / 60);

            timer.innerHTML = "" + minutes + ":" + secondsTens + secondsOnes;
        }


        function onDocumentKeyDown(event) {
            var keyCode = event.which;
            play.keydown(keyCode);
            if (keyCode == 20)
            {
                scoreboard.style.display = 'flex'
                sortTable()    
            }
        };

        function onDocumentKeyUp(event) {
            var keyCode = event.which;
            play.keyup(keyCode);
            if (keyCode == 20)
                scoreboard.style.display = 'none'
        };

        //#endregion

        function sortTable(){
            var tableData = document.getElementById("score_table").getElementsByTagName('tbody').item(0);
            var rowData = tableData.getElementsByTagName('tr');
            for(var i = 0; i < rowData.length - 1; i++){
                for(var j = 0; j < rowData.length - (i + 1); j++){
                    if(Number(rowData.item(j).getElementsByTagName('td').item(1).innerHTML.replace(/[^0-9\.]+/g, "")) < Number(rowData.item(j+1).getElementsByTagName('td').item(1).innerHTML.replace(/[^0-9\.]+/g, ""))){
                        tableData.insertBefore(rowData.item(j+1),rowData.item(j));
                    }
                }
            }
        }


        
        
        
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
            if (boostreload > 0)
                boostreload -= dt * 400;
            else
                boostreload = 0
            if (reload > 0)
            {
                reload -= dt * 400;
                circle.style.background = `conic-gradient(#cccccc ${360 - reload}deg, rgba(1.0, 1.0, 1.0, 0.0) 0deg)`
            }
            else
            {
                reload = 0;
                circle.style.background = `conic-gradient(#cccccc 0deg, rgba(1.0, 1.0, 1.0, 0.0) 0deg)`
            }
            play.update(dt);
            players.forEach(element => {
				element.update(dt);
			});
            sh.material.uniforms.time.value = t;
            tor.material.uniforms.time.value = t + 1;
            toru.material.uniforms.time.value = t + 2;
            if (Math.tan(sh.material.uniforms.time.value) > 2.0 && !scene.getObjectByName('flag'))
                    scene.remove(sh)
            if (Math.tan(tor.material.uniforms.time.value) > 2.0 && !scene.getObjectByName('flag'))
                    scene.remove(tor)
            if (Math.tan(toru.material.uniforms.time.value) > 2.0 && !scene.getObjectByName('flag'))
                    scene.remove(toru)
            renderer.render( scene, camera );
        }
        animate(); 
    })();
    });

    onDestroy(() => {
		if (chatSocket)
            chatSocket.close()
	})
</script>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');
    #ui {
        position: absolute;
		width: 10px;
		height: 10px;
    }
    #blocker {
        /*border-radius: 3% !important;*/
        z-index: 2;
		position: absolute;
		width: 100%;
		height: 100%;
		background-color: rgba(0,0,0,0.3);
	}
    #crosshair {
        position: absolute;
        top: 50%;
        left: 50%;
        z-index: 1;
        pointer-events: none;
    }
    #crossimg {
        pointer-events: none;
        width: 50%;
        position: relative;
        transform: translate(-50%, -50%);
    }

    #timer {
        position: absolute;
        left: 50%;
        transform: translate(-50%);
    }

    #circular {
        pointer-events: none;
        position: absolute;
        width: 30px;
        height: 30px;
        top: -15px;
        left: -15px;
        border-radius: 50%;
        background: conic-gradient(#cccccc 0deg, rgba(1.0, 1.0, 1.0, 0.0) 0deg);
    }

    .text {
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


    .game {
        /*border-radius: 3% !important;*/
        margin: auto !important;
    }

    #flagicon {
        display: none;
    }



    #scoreboard {
        pointer-events: none;
        height: 400px;
        display: none;
        align-items: center;
        justify-content: center;
    }

    table {
        border: 1px solid rgba(0,0,0,0);
        color: white;
    }
    :global(tr > td:nth-child(even)) {
      background-color: rgba(255, 101, 101, 0.7);
    }
    :global(tr > td:nth-child(odd)) {
      background-color: rgba(252, 67, 67, 0.7);
    }
    :global(tr) {
        border-top: 1px solid rgb(112, 112, 112);
        border-bottom: 1px solid rgb(112, 112, 112);
    }
    th {

        background-color: rgba(54, 54, 54, 0.7);
    }

</style>

<div id="ui">
    <div id="blocker">
    </div>
    <div>
        <img id="flagicon" alt="flag" src="src/routes/(private)/shooter/public/flag.png"/>
        <span class="text" id="timer"></span>
    </div>
    <div id="crosshair">
        <div id="circular"></div>
        <img id="crossimg" alt="ch" src="src/routes/(private)/shooter/public/dotcrosshair.png"/>
    </div>
    <div id="scoreboard">
        <table id="score_table">
            <thead>
                <tr>
                    <th scope="col">Username</th>
                    <th scope="col">Score</th>
                </tr>
            </thead>
            <tbody id="mytbody">
            </tbody>
        </table>
    </div>
</div>

<!-- <canvas id="canvas" class="d-flex flex-column game"></canvas> -->
<canvas bind:this={canvas} class="d-flex flex-column game"></canvas>