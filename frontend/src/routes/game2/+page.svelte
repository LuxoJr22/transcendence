<script lang= "ts">
    import { onMount } from 'svelte';
    import * as THREE from 'three';
    import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
    import { GUI } from 'three/addons/libs/lil-gui.module.min.js';
    import { label } from 'three/examples/jsm/nodes/Nodes.js';
    import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
    import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
    import { AfterimagePass } from 'three/addons/postprocessing/AfterimagePass.js';
	import { RenderPixelatedPass } from 'three/addons/postprocessing/RenderPixelatedPass.js';
    import * as SkeletonUtils from 'three/examples/jsm/utils/SkeletonUtils.js';
    import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
    import { Shooter } from "./shooter.js";
    import { Player } from "./player.js";
    import { shade } from "./watershader";
    let canvas;
    var scoring = 0;
    export var ls = 0;

    onMount(() => { (async () => {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.1, 1000 );
        camera.position.z = 3;
        camera.position.y = 0.5;

        var el = document.getElementById("blocker");


        scene.background = new THREE.Color(0x54A0E4);

        
        var bind2 = {up: 90, down: 83, left:81, right:68, jump:32}
        var bind = {up: 40, down: 38, left:39, right:37, jump:96}

        //#region LoadModel

        const loader = new GLTFLoader()


        const gltf = await loader.loadAsync('src/routes/game2/public/pop.glb');


        gltf.scene.position.set(-10, 0, -1.5);
        gltf.scene.scale.set(0.5, 0.5, 0.5);

        var play = new Shooter(gltf, bind2, 0.15, camera, scene);
        //scene.add(play.mesh);

        el.addEventListener('click', function () {
            el.style.display = "none";
            play.cam.lock();
        });


        play.cam.addEventListener( 'unlock', function () {
            el.style.display = '';

        } );

        scene.add(play.cam.getObject());


        const gl = await loader.loadAsync('src/routes/game2/public/sty.glb');

        gl.scene.position.set(10, 0, -1.5);
        gl.scene.scale.set(0.5, 0.5, 0.5);

        var er = new Player(gl, bind, 0.15, 0);
        scene.add(er.mesh);



        //#endregion

        const plain = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), shade);

        plain.position.set(0, -1, 0);
        plain.rotation.x = -Math.PI / 2
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
        renderer.setSize( 1920 * 0.7 , 1080 * 0.7);
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
        }

        function onMouse(event) {
            if (event.which == 1)
                play.mousedown();
        }

        function onDocumentKeyDown(event) {
            var keyCode = event.which;
            play.keydown(keyCode);
            er.keydown(keyCode);
        };

        function onDocumentKeyUp(event) {
            var keyCode = event.which;
            play.keyup(keyCode);
            er.keyup(keyCode);
        };

        //#endregion

        let t = 0;
        const clock = new THREE.Clock();


        //#endregion

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
            if (play.canmove)
            {
                play.move();
            }
            er.update(dt)
            if (er.canmove)
            {
                er.move();
            }
            renderer.render( scene, camera );
        }
        animate(); 
    })();
    });
</script>

<style>
    #blocker {
				position: absolute;
				width: 100%;
				height: 100%;
				background-color: rgba(0,0,0,0.1);
			}
    #crosshair {
        position: absolute;
        top: 415px;
        bottom: 0;
        left: 625px;
        right: 0;
        width: 5%;
        z-index: 1;
    }

</style>

<div id="blocker">
</div>
<img id="crosshair" src="src/routes/game2/public/ch.png"/>
<canvas bind:this={canvas} class=""></canvas>