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
    import { Player } from "./player.js";
    import { shade } from "./watershader";
    let canvas;

    onMount(() => { (async () => {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.1, 1000 );
        scene.background = new THREE.Color(0x54A0E4);

        var bind = {up: 83, down: 90, left:68, right:81, charge:32}
        var bind2 = {up: 38, down: 40, left:37, right:39, charge:96}
        var limit = {px: 0, py:8, nx:-18, ny:-8}
        var limit2 = {px: 18, py:8, nx: 0, ny:-8}


        //#region LoadModel

        const loader = new GLTFLoader()

        const gltf = await loader.loadAsync('src/routes/game/public/pop.glb');
        gltf.scene.position.set(-10, 0, -1.5);
        gltf.scene.scale.set(0.5, 0.5, 0.5);
        gltf.scene.rotation.y = Math.PI / 2;
        gltf.scene.rotation.x = Math.PI / 2;


        var play = new Player(gltf, bind2, limit, 0.15);

        scene.add(play.mesh);

        const gl = await loader.loadAsync('src/routes/game/public/sty.glb');
        gl.scene.position.set(10, 0, -1.5);
        gl.scene.scale.set(0.5, 0.5, 0.5);
        gl.scene.rotation.y = Math.PI * 3 / 2;
        gl.scene.rotation.x = Math.PI / 2;

        var er = new Player(gl, bind, limit2, 0.15);

        scene.add(er.mesh);


        const bouee = await loader.loadAsync('src/routes/game/public/bue.glb');
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




        const textur = new THREE.TextureLoader().load( "src/routes/game/public/f.png" );

        textur.wrapS = THREE.RepeatWrapping;

        textur.wrapT = THREE.RepeatWrapping;

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
        renderer.setSize( 1920 * 0.7 , 1080 * 0.7);
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
            if (window.innerWidth * 0.7 < 1920 * 0.7)
                renderer.setSize( window.innerWidth * 0.70, (window.innerWidth * 0.70) / 16 * 9);
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

        const controls = new OrbitControls( camera, renderer.domElement );
                        controls.target.set( 0, 0, 0 );
                        controls.update();

        //#endregion

        let t = 0;
        const clock = new THREE.Clock();

        let balldir = -0.1;
        let balldiry = 0


        //#region MoveBall

        function moveBall()
        {
            sphere.translateX(balldir);
            sphere.translateY(balldiry);
            if (sphere.position.x >= 15 || sphere.position.x <= -15)
            {
                if (sphere.position.x >= 15)
                    play.point ++;
                else
                    er.point ++;
                sphere.position.set(0, 0, 0);
                er.mesh.position.set(10, 0, -1.5);
                play.mesh.position.set(-10, 0, -1.5);
                play.reset();
                balldiry = 0
            }
            if (sphere.position.y >= 7 || sphere.position.y <= -7 )
                balldiry *= -1;

        }

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

        //#endregion

        var composer = new EffectComposer( renderer );
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
            if (play.canmove)
            {
                play.move();
            }
            er.update(dt)
            if (er.canmove)
            {
                er.move();
            }
            moveBall();
            checkCollision();
            renderer.render( scene, camera );
        }
        animate(); 
    })();
    });
</script>

<canvas bind:this={canvas} class=""></canvas>