<script lang="ts">
    import * as THREE from 'three';
    import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
    import { Shooter } from "$lib/stores/shooter/shooter";
    import { Player } from "$lib/stores/shooter/player";
    import { flagshader } from "$lib/stores/shooter/flagshader";
    import { createmap } from "$lib/stores/shooter/map"
    import { auth, fetchUser, getAccessToken } from '$lib/stores/auth';
	import type { AuthState } from '$lib/stores/auth';
    import { goto, beforeNavigate, afterNavigate } from '$app/navigation';

	let state: AuthState;
	$: $auth, state = $auth;
    var chatSocket: WebSocket | null;
    let isLoad : boolean = false;


    let isEnded = false;
    let endingscreen = 0;

    window.onbeforeunload = () => {
        if (chatSocket) {
            chatSocket.close();
            chatSocket = null;
        }
    };


    afterNavigate(() => { (async () => {
        if (!isLoad)
            isLoad = true;
        else
            return ;
        await fetchUser();
        auth.subscribe((value : AuthState) =>{
            state = value;
        });

        var match_id
        let accessToken = await getAccessToken();
        if (accessToken == null)
            return ;
        const response = await fetch('/api/shooter/create/', {
		method: 'POST',
		headers: { 'Authorization': `Bearer ${accessToken}` },
		});
		const data = await response.json();
		if (response.ok)
		{
			match_id = data.match
		}

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera( 70, 16 / 9, 0.1, 1000 );


        const camer = new THREE.PerspectiveCamera( 70, 16 / 9, 0.1, 1000 );
        
        var pointerLockActivated = 0

        let t = 0;
        const clock = new THREE.Clock();
        var reload = 0;
        var boostreload = 0

        var canvas = document.getElementById("canvas")
        var el = document.getElementById("blocker");
        var ui = document.getElementById("ui");
        var circle = document.getElementById("circular");
        var ficon = document.getElementById("flagicon");
        var scoreboard = document.getElementById("scoreboard")
        var crosshair = document.getElementById("crosshair")
        var timer = document.getElementById("timer")
        var table_body : HTMLTableElement = document.getElementById("mytbody")! as HTMLTableElement
        var play_btn = document.getElementById("play_btn") as HTMLButtonElement
        var menu_btn = document.getElementById("menu_btn") as HTMLButtonElement


        var score_row = new Map()

        var players : Player[] = []


        scene.background = new THREE.Color(0x54A0E4);

        var menu_displayed = true;
        
        var bind = {up: 90, down: 83, left:81, right:68, jump:32}

        const resp = await fetch('/api/shooter/settings/' + state.user?.id, {
		method: 'GET',
		headers: { 'Authorization': `Bearer ${accessToken}` },
		});
		const dat = await resp.json();
		if (resp.ok)
		{
			bind = dat.settings
		}


        var id = 0
        const loader = new GLTFLoader()
        
        createmap(scene, loader);


        const sh = new THREE.Mesh(new THREE.TorusGeometry(1.5, 0.1, 20), flagshader)
        sh.rotation.x = Math.PI / 2;
        sh.position.set(0, 9, -5)
        scene.add(sh)

        const tor = new THREE.Mesh(new THREE.TorusGeometry(1.5, 0.1, 20), flagshader.clone())
        tor.rotation.x = Math.PI / 2;
        tor.position.set(0, 9, -5)
        scene.add(tor)

        const toru = new THREE.Mesh(new THREE.TorusGeometry(1.5, 0.1, 20), flagshader.clone())
        toru.rotation.x = Math.PI / 2;
        toru.position.set(0, 9, -5)
        scene.add(toru)


        

        const flag = await loader.loadAsync('/assets/maps/shooter/f.glb');
        flag.scene.name = 'flag'
        flag.scene.position.set(0, 8, -5);




        var play = new Shooter(bind, 0.15, camera, scene);
        
            //scene.add(play.mesh);

        play_btn!.addEventListener('click',  function() {
            let now = performance.now()
            if (isEnded)
            {
                menu_displayed = false
                el!.style.opacity = "0";
                el!.style.display = 'none';
                menu_btn!.disabled = true
                play_btn!.disabled = true
                return
            }
            if ((pointerLockActivated && now - pointerLockActivated < 1100))
                return
            menu_displayed = false
            el!.style.opacity = "0";
            el!.style.display = 'none';
            menu_btn!.disabled = true
            play_btn!.disabled = true
            play.cam.lock();
        });

        menu_btn!.addEventListener('click',  function() {
            if (chatSocket)
                chatSocket.close();
            goto('/');
        });


        play.cam.addEventListener( 'unlock', function () {
            if (isEnded)
                return
            pointerLockActivated = performance.now()
            play.controller.xp = 0;
            play.controller.xn = 0;
            play.controller.yp = 0;
            play.controller.yn = 0;
            menu_btn!.disabled = false
            play_btn!.disabled = false
            menu_displayed = true
            scoreboard!.style.display = 'none'
            el!.style.opacity = "1";
            el!.style.display = '';
        } );

        const gg = await loader.loadAsync('/assets/ui/shooter/nerf_gun.glb');
        gg.scene.scale.set(0.005, 0.005, 0.005)
        gg.scene.position.set(1, -0.5, 0)
        play.cam.getObject().attach(gg.scene)

        scene.add(play.cam.getObject());



        //#endregion





        const renderer = new THREE.WebGLRenderer({canvas, antialias: false});
        var canvasSize = {width: (window.innerHeight) * 16 / 9,  height: (window.innerHeight)}
        if (canvasSize.width > window.innerWidth)
        {
            canvasSize.width =  (window.innerWidth)
            canvasSize.height =  (window.innerWidth) * 9 / 16
        }
        renderer.setSize( canvasSize.width, canvasSize.height);
        ui!.style.width = canvasSize.width + "px";
        ui!.style.height = canvasSize.height + "px";
        ui!.style.top = renderer.domElement.getBoundingClientRect().top + "px"
        ui!.style.left = renderer.domElement.getBoundingClientRect().left + "px"
        timer!.style.fontSize = canvasSize.height / 10 + "px"
        play_btn!.style.fontSize = canvasSize.height / 15 + "px"
        play_btn!.style.width = canvasSize.width / 3 + "px"
        play_btn!.style.height = canvasSize.height / 10 + "px"
        menu_btn!.style.fontSize = canvasSize.height / 15 + "px"
        menu_btn!.style.width = canvasSize.width / 3 + "px"
        menu_btn!.style.height = canvasSize.height / 10 + "px"
        renderer.shadowMap.enabled = true;
        document.body.appendChild( renderer.domElement );
        ui!.style.display = 'block'

        var xSpeed = 0.15;
        var ySpeed = 0.15;

        //#region CommandHandler

        document.addEventListener("keydown", onDocumentKeyDown, false);
        document.addEventListener("keyup", onDocumentKeyUp, false);
        document.addEventListener("mousedown", onMouse, false);

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


        function handlesticks(axes : Gamepad["axes"])
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
            ui!.style.width = canvasSize.width + "px";
            ui!.style.height = canvasSize.height + "px";
            ui!.style.top = renderer.domElement.getBoundingClientRect().top + "px"
            ui!.style.left = renderer.domElement.getBoundingClientRect().left + "px"
            timer!.style.fontSize = canvasSize.height / 10 + "px"
            play_btn!.style.fontSize = canvasSize.height / 15 + "px"
            play_btn!.style.width = canvasSize.width / 3 + "px"
            play_btn!.style.height = canvasSize.height / 10 + "px"
            menu_btn!.style.fontSize = canvasSize.height / 15 + "px"
            menu_btn!.style.width = canvasSize.width / 3 + "px"
            menu_btn!.style.height = canvasSize.height / 10 + "px"


            
        }

        
        function onMouse(event : MouseEvent) {
            if (event.which == 1 && menu_displayed == false)
            {
                shoot()
            }
            if (event.which == 3 && menu_displayed == false)
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
                        chatSocket!.send(JSON.stringify({
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

        async function createPlayer(play_id : number, skin : string) {
            const gl = await loader.loadAsync('/assets/skins/' + skin);
            gl.scene.position.set(10, 0, -1.5);
            gl.scene.scale.set(0.5, 0.5, 0.5);
            let pl = new Player(gl, 0.15, scene, play_id)
            play.target = play.target.concat(pl.target)
            const gun = await loader.loadAsync('/assets/ui/shooter/nerf_gun.glb');
            gun.scene.scale.set(0.005, 0.005, 0.005)
            gun.scene.rotation.y = Math.PI
            gun.scene.position.set(8.5, 1.5, -1)
            pl.bone.attach(gun.scene)
            players.push(pl);
        }

        let url = '/ws/shooter/shooter_' + match_id + '/?token=' + accessToken;
        
        chatSocket = new WebSocket(url);
        
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
                    var row = table_body!.insertRow()
                    var usercell = row.insertCell(0)
                    var scorecell = row.insertCell(1)

                    usercell.innerHTML = data.players[i].username
                    scorecell.innerHTML = `${Math.round(data.players[i].score)}`
                    score_row.set(i, row)
                    i ++;
                }
                camera.position.z = data.position.z;
                camera.position.y = data.position.y;
                camera.position.x = data.position.x;
                camera.rotation.x = data.rotation.x;
                camera.rotation.y = data.rotation.y;
                camera.rotation.z = data.rotation.z;

                chatSocket!.send(JSON.stringify({
					'event':'frame',
					'player':[play.cam.getObject().position, play.direction],
                    'controller':play.controller,
                    'id':id
				}))
			}
            else if (data.event == 'Connected' && id != data.id)
            {
                let i = 0
                while (players[i])
                {
                    if (players[i].id == data.id - 1) {
                        players[i].target.forEach((el : THREE.Object3D) => {scene.remove(el)})
                        players[i].mesh.geometry = undefined
                        players[i].mesh.material = undefined
                        scene.remove(players[i].mesh)
                        players.splice(i, 1)

                        table_body!.removeChild(score_row.get(data.id - 1))
                        score_row.delete(data.id - 1)
                    }
                    i ++
                }
                createPlayer(data.id - 1, data.players[data.id - 1].skin)

                var row = table_body!.insertRow()
                var usercell = row.insertCell(0)
                var scorecell = row.insertCell(1)
                usercell.innerHTML = data.players[data.id - 1].username
                scorecell.innerHTML = `${Math.round(data.players[data.id - 1].score)}`
                score_row.set(data.id - 1 , row)
            }
            if (data.event == 'Flag_picked')
            {
                if (data.id == id)
                    ficon!.style.display = "block";
                scene.remove(flag.scene);
            }
            if (data.event == 'Flag_dropped')
            {
                if (data.id == id)
                    ficon!.style.display = "none";
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
                    score_row.get(actid).children[1]!.innerHTML = `${Math.round(data.players[actid].score)}`
                    i ++;
                }
                score_row.get(id - 1).children[1]!.innerHTML = `${Math.round(data.players[id - 1].score)}`
				chatSocket!.send(JSON.stringify({
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
            {
                scoreboard!.style.display = 'flex'
                sortTable()    
                isEnded = true
                play.cam.unlock()
                crosshair!.style.display = "none"
                timer!.innerHTML = data.username + " won the game!"
                if (chatSocket)
                    chatSocket.close()
            }
        }

        function timer_update(totalSeconds : number)
        {
            if (totalSeconds < 0)            
                totalSeconds = 0
            let seconds = totalSeconds % 60;
            let secondsTens = Math.floor(seconds / 10);
            let secondsOnes = seconds % 10;
            let minutes = Math.floor(totalSeconds / 60);

            timer!.innerHTML = "" + minutes + ":" + secondsTens + secondsOnes;
        }


        function onDocumentKeyDown(event : KeyboardEvent) {
            if (menu_displayed == false)
            {
                var keyCode = event.which;
                if (keyCode == 9) {
                    event.preventDefault();
                }
                play.keydown(keyCode);
                if (keyCode == 9)
                {
                    scoreboard!.style.display = 'flex'
                    sortTable()    
                }
            }
        };

        function onDocumentKeyUp(event : KeyboardEvent) {
            if (menu_displayed == false)
            {
                var keyCode = event.which;
                play.keyup(keyCode);
                if (keyCode == 9 && isEnded == false)
                    scoreboard!.style.display = 'none'
            }
        };

        //#endregion

        function sortTable(){
            var tableData = document.getElementById("score_table")!.getElementsByTagName('tbody').item(0);
            var rowData = tableData!.getElementsByTagName('tr');
            for(var i = 0; i < rowData.length - 1; i++){
                for(var j = 0; j < rowData.length - (i + 1); j++){
                    if(Number(rowData.item(j)!.getElementsByTagName('td').item(1)!.innerHTML.replace(/[^0-9\.]+/g, "")) < Number(rowData.item(j+1)!.getElementsByTagName('td').item(1)!.innerHTML.replace(/[^0-9\.]+/g, ""))){
                        tableData!.insertBefore(rowData.item(j+1)!,rowData.item(j));
                    }
                }
            }
        }

        chatSocket.onclose = function(e) {
			if (e.code != 1000)
				goto('/');
        }


        function gameLogic(dt :number)
        {
            if (gamepads[0])
            {
                gamepads[0] = navigator.getGamepads()[0]!
                handlebuttons(gamepads[0].buttons)
                handlesticks(gamepads[0].axes)
            }
            if (boostreload > 0)
            {
                boostreload -= dt * 400;
                gg.scene.position.z = boostreload / 300
            }
            else
            {
                boostreload = 0
            }
            if (reload > 0)
            {
                reload -= dt * 400;
                gg.scene.rotation.x = reload / 400
                circle!.style.background = `conic-gradient(#cccccc ${360 - reload}deg, rgba(1.0, 1.0, 1.0, 0.0) 0deg)`
            }
            else
            {
                gg.scene.rotation.x = 0;
                reload = 0;
                circle!.style.background = `conic-gradient(#cccccc 0deg, rgba(1.0, 1.0, 1.0, 0.0) 0deg)`
            }
            play.update(dt);
            players.forEach(element => {
				element.update(dt);
			});
            renderer.render( scene, camera );
        }
        
        
        function animate() {
            if (isLoad)
                requestAnimationFrame( animate );
            const dt = clock.getDelta();
            t += dt;
            sh.material.uniforms.time.value = t;
            tor.material.uniforms.time.value = t + 1;
            toru.material.uniforms.time.value = t + 2;
            if (Math.tan(sh.material.uniforms.time.value) > 2.0 && !scene.getObjectByName('flag'))
                    scene.remove(sh)
            if (Math.tan(tor.material.uniforms.time.value) > 2.0 && !scene.getObjectByName('flag'))
                    scene.remove(tor)
            if (Math.tan(toru.material.uniforms.time.value) > 2.0 && !scene.getObjectByName('flag'))
                    scene.remove(toru)
            if (isEnded == false)
                gameLogic(dt)
            else
            {
                camer.position.set(0, 80, 0)
                camer.rotation.set(-Math.PI / 2, 0, 0)
                endingscreen += dt
                if (endingscreen >= 10)
                    goto('/')
                renderer.render( scene, camer );
            }
            
        }
        animate(); 
    })();
    });

    beforeNavigate(() => {
        isLoad = false
		if (chatSocket)
            chatSocket.close()
	})

</script>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Luckiest+Guy&display=swap');
    #ui {
        display: none;
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
		background-color: rgba(0,0,0,0.4);
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
        pointer-events: none;
  		font-style: normal;
		color:white;
		font-size: 70px;
		text-shadow:
		2px 2px 0 #000,
		-2px 2px 0 #000,
		-2px -2px 0 #000,
		2px -2px 0 #000;
	}

    .text_menu {
		font-family: "Luckiest Guy", cursive;
  		font-style: normal;
		color:white;
        padding: 0%;
		font-size: 40px;
        margin-top: 0%;
	}


    .game {
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
        z-index: 4;
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
    th:first-child{
        width: 100px;
    }

</style>

<div id="ui">
    <div id="blocker" class="d-flex align-items-center flex-column ">
        <button class="btn btn-dark btn-lg border m-0 p-0 mb-1 position-relative text_menu" style="top:45%" id="play_btn">Play</button>
        <button class="btn btn-dark btn-lg border m-0 p-0 mb-1 position-relative text_menu" style="top:45%" id="menu_btn">BACK TO MENU</button>
    </div>
    <div>
        <img id="flagicon" alt="flag" src="assets/ui/shooter/flag.png"/>
        <span class="text" id="timer"></span>
    </div>
    <div id="crosshair">
        <div id="circular"></div>
        <img id="crossimg" alt="ch" src="assets/ui/shooter/dotcrosshair.png"/>
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

<canvas id="canvas" class="d-flex game"></canvas>
<!-- <canvas bind:this={canvas} class="d-flex flex-column game"></canvas> -->