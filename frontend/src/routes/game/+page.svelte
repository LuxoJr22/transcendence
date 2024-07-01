<script lang= "ts">
    import { onMount } from 'svelte';
    import * as THREE from 'three';
    import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
    import { CSS2DRenderer , CSS2DObject} from 'three/addons/renderers/CSS2DRenderer.js';
    import { GUI } from 'three/addons/libs/lil-gui.module.min.js';
    import { label } from 'three/examples/jsm/nodes/Nodes.js';
    import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
    import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
    import { AfterimagePass } from 'three/addons/postprocessing/AfterimagePass.js';
    let scene, camera, renderer;
    let cube;
    let canvas;

    onMount(() => { (async () => {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.1, 1000 );
        scene.background = new THREE.Color(0x449977);

        //#region PlayerClass

        class Player {
            constructor (mesh, bind, limit) {
                this.mesh = mesh.scene;
                this.mixer = new THREE.AnimationMixer( mesh.scene );
                this.bb = new THREE.Box3().setFromObject( mesh.scene);
                this.left = this.mesh.getObjectByName("Bone003L");
                this.right = this.mesh.getObjectByName("Bone003R");
                this.bone = this.mesh.getObjectByName("Bone");
                this.gamepad = 0;
                this.point = 0;
                this.dir = 0;

                this.animleg = 0

                this.canmove = 1;
                this.isfalling = 0;
                this.charging = 1;
                this.knockback = 0;
            
                this.limit = limit;
                this.bind = bind;
                let load = this.mixer.clipAction( gltf.animations[ 1 ] );
                let fall = this.mixer.clipAction( gltf.animations[ 2 ] );
                load.setLoop(THREE.LoopOnce);
                load.clampWhenFinished = true;
                fall.setLoop(THREE.LoopOnce);
                this.anims = {load: load, fall: fall};
                this.charge = 0;

                this.controller = {xp: 0, xn: 0, yp: 0, yn: 0, charge: 0}
            }
            update (dt) {
                this.knockback = THREE.MathUtils.lerp(this.knockback, 0, 0.1)
                this.action();
                if (this.charge && this.anims.load.time < 0.1 && !this.isfalling)
                {
                    this.animleg = -Math.PI / 2;
                    this.left.rotation.z = -Math.PI / 2;
                    this.right.rotation.z = Math.PI / 2;
                    this.left.rotation.y = 0;
                    this.right.rotation.y = 0;
                    this.left.rotation.x = 0;
                    this.right.rotation.x = 0;
                }
                if (this.isfalling && this.anims.fall.time > 0.2 && this.anims.fall.time < 0.4)
                    this.charge = 0;
                if (this.isfalling && this.anims.fall.time > 0.6)
                {
                    this.canmove = 0;
                    this.charge = 1;
                }
                if (this.isfalling && !this.anims.fall.enabled)
                {
                    this.isfalling = 0;
                    this.charge = 0;
                    this.anims.fall.stop();
                    this.canmove = 1
                }
                this.mixer.update( dt );
                if (this.charge)
                {
                    this.charging = THREE.MathUtils.lerp(this.charging, 5, 0.05)
                    if (this.anims.load.paused)
                    {
                        this.anims.fall.play();
                        this.anims.load.stop()
                        this.isfalling = 1;
                    }
                }
                else
                    this.charging = THREE.MathUtils.lerp(this.charging, 1, 0.1)
            }
            movelegs()
            {
                let diry = this.controller.yn + this.controller.yp;
                let dirx = this.controller.xn + this.controller.xp;

                if (dirx != 0)
                    this.dir = Math.atan(diry / dirx);
                else
                    this.dir = Math.asin(diry * 10);
                if (this.charge == 0)
                {
                    if (dirx == 0 && diry == 0)
                        this.animleg = 0;
                    else if (this.animleg == 0)
                        this.animleg = Math.PI / 3;
                    if (this.animleg != 0 && Math.abs(this.left.rotation.z) >= Math.abs(this.animleg) - 0.1)
                        this.animleg *= -1;

                    /*if ( this.left.rotation.z > 0)
                        this.bone.position.y = -this.left.rotation.z / 2;
                    else
                        this.bone.position.y = this.left.rotation.z / 2;*/
                    this.left.rotation.y = -this.dir;
                    this.right.rotation.y = -this.dir;
                    this.left.rotation.x = 0;
                    this.right.rotation.x = 0;
                    this.left.rotation.z = THREE.MathUtils.lerp(this.left.rotation.z, this.animleg, 0.1)
                    this.right.rotation.z = THREE.MathUtils.lerp(this.right.rotation.z, this.animleg, 0.1)
                }
                else
                {
                    if (dirx == 0 && diry == 0)
                        this.animleg = -Math.PI / 2;
                    else if (this.animleg == -Math.PI / 2)
                        this.animleg = -Math.PI / 3;
                    if (this.animleg != -Math.PI / 2 && Math.abs(this.left.rotation.z + Math.PI / 2) >= Math.abs(this.animleg + Math.PI / 2) - 0.05)
                    {
                        if (this.animleg == -Math.PI / 3)
                            this.animleg = -2 * Math.PI / 3;
                        else if (this.animleg == -2 * Math.PI / 3)
                            this.animleg = -Math.PI / 3;
                    }
                    this.left.rotation.x = -this.dir;
                    this.right.rotation.x = this.dir;
                    this.left.rotation.y = 0;
                    this.right.rotation.y = 0;
                    this.left.rotation.z = THREE.MathUtils.lerp(this.left.rotation.z, this.animleg, 0.1)
                    this.right.rotation.z = THREE.MathUtils.lerp(this.right.rotation.z, this.animleg + Math.PI, 0.1)
                }
            }
            move () {
                this.movelegs();
                let ym, xm;
                this.bb = new THREE.Box3().setFromObject(this.mesh);
                xm = this.controller.xn + this.controller.xp + this.knockback;
                ym = this.controller.yn + this.controller.yp;

                if (this.charge)
                {
                    ym /= 2;
                    xm /= 2;
                }
                if (this.mesh.position.y + ym > this.limit.ny && this.mesh.position.y + ym < this.limit.py)
                {
                    this.mesh.translateX(ym);
                }
                if (this.mesh.position.x + xm > this.limit.nx && this.mesh.position.x + xm < this.limit.px)
                {
                    this.mesh.translateZ(xm);
                }
            }
            keydown (keyCode) {
                if (keyCode == this.bind.up)
                    this.controller.yp = ySpeed;
                if (keyCode == this.bind.down)
                    this.controller.yn = -ySpeed;
                if (keyCode == this.bind.left)
                    this.controller.xn = -xSpeed;
                if (keyCode == this.bind.right)
                    this.controller.xp = xSpeed;
                if (keyCode == this.bind.charge)
                {
                    this.controller.charge = 1;
                }
            }
            keyup (keyCode) {
                if (keyCode == this.bind.up)
                    this.controller.yp = 0;
                if (keyCode == this.bind.down)
                    this.controller.yn = 0;
                if (keyCode == this.bind.left)
                    this.controller.xn = 0;
                if (keyCode == this.bind.right)
                    this.controller.xp = 0;

                if (keyCode == this.bind.charge)
                {
                    this.controller.charge = 0;
                }
            }
            action() {
                if (this.controller.charge == 1 && !this.isfalling)
                {
                    this.anims.load.play();
                    this.charge = 1;
                }
                if (this.controller.charge == 0 && !this.isfalling)
                {
                    this.charge = 0;
                    this.anims.load.stop();
                }
            }
            reset() {
                this.anims.fall.stop();
                this.anims.load.stop();
                this.isfalling = 0;
            }
        }
        //#endregion


        var bind = {up: 83, down: 90, left:68, right:81, charge:32}
        var bind2 = {up: 40, down: 38, left:39, right:37, charge:96}
        var limit = {px: 0, py:8, nx:-18, ny:-8}
        var limit2 = {px: 18, py:8, nx: 0, ny:-8}


        //#region LoadModel

        const loader = new GLTFLoader()

        const gltf = await loader.loadAsync('src/routes/game/public/pop.glb');
        gltf.scene.position.set(-10, 0, -1.5);
        gltf.scene.scale.set(0.5, 0.5, 0.5);
        gltf.scene.rotation.y = Math.PI / 2;
        gltf.scene.rotation.x = Math.PI / 2;


        var play = new Player(gltf, bind2, limit);

        scene.add(play.mesh);

        const gl = await loader.loadAsync('src/routes/game/public/sty.glb');
        gl.scene.position.set(10, 0, -1.5);
        gl.scene.scale.set(0.5, 0.5, 0.5);
        gl.scene.rotation.y = Math.PI * 3 / 2;
        gl.scene.rotation.x = Math.PI / 2;

        var er = new Player(gl, bind, limit2);

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


        const {generateCausticCanvasTexture} = await import("./waterTexture.js");
        const mapping = generateCausticCanvasTexture(15);


        const shade = new THREE.ShaderMaterial( {
            uniforms: {
            map : {value: mapping},
            basecolor : {value: new THREE.Color(0x19ABFF)},
            foamcolor : {value: new THREE.Color(0xffffff)},
            time: { value : 1.0},
            scale: { value : 10.0},
            },
            fragmentShader: `
            varying vec2 vUv;
            varying vec3 vposition;
            uniform sampler2D map;
            uniform vec3 basecolor;
            uniform vec3 foamcolor;
            uniform float time;
            uniform float scale;

            void main() {
                int p = int(((time / 50.0) - floor(time / 50.0)) * 10.0);
                gl_FragColor.a = 1.0;
                vec3 color = texture2D( map, vUv * scale +
                    0.5*vec2( cos(time*0.001*0.1), sin(time*0.001*0.1)) +
                    0.1*vec2( cos(time*0.0012+3.2*scale*vUv.x), sin(time*0.001+3.0*scale*vUv.y))).rgb;
                vec3 color2 = texture2D( map, vUv * scale * 1.3+
                    0.8*vec2(cos(time*0.001*0.1), sin(time*0.001*0.1)) +
                    0.01*vec2(cos(1.7 + time*0.0012+3.2*scale*vUv.x), sin(1.7 + time*0.001+3.0*scale*vUv.y))).rgb;
                float d = 0.0;
                gl_FragColor.rgb = mix(basecolor * clamp(1.0 - color2, 0.9, 1.0), foamcolor, color.r);
                    
            }`,
            vertexShader: `
            varying vec2 vUv;
            varying vec3 vposition;
            void main() {
                vUv = uv;
                vposition = (modelMatrix * vec4(position, 1.0)).xyz;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);	
            }
            `
        });


        const textur = new THREE.TextureLoader().load( "src/routes/game/public/f.png" );

        textur.wrapS = THREE.RepeatWrapping;

        textur.wrapT = THREE.RepeatWrapping;

        let me = new THREE.MeshLambertMaterial({ map : textur });

        const plain = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), shade);

        plain.position.set(0, 0, -0.8);
        plain.overdraw = true;
        plain.receiveShadow = true;

        scene.add(plain);

        //#endregion


        const light = new THREE.AmbientLight(0xffffff)
        scene.add(light)

        const dl = new THREE.DirectionalLight( 0xffffff, 3 );
        dl.position.set( 0, 0, 5 );
        scene.add( dl );



        const renderer = new THREE.WebGLRenderer({canvas});
        renderer.setSize( 1920 * 0.7 , 1080 * 0.7);
        // renderer.domElement.style.width = window.innerWidth * 0.50 + "px";
        // renderer.domElement.style.height = window.innerHeight * 0.50 + "px";
        document.body.appendChild( renderer.domElement );

        camera.position.z = 20;

        var xSpeed = 0.1;
        var ySpeed = 0.1;


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
                c.textContent = er.point;
                p.textContent = play.point;
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
        composer.addPass( new RenderPass( scene, camera ) );

        var afterimagePass = new AfterimagePass();
        composer.addPass( afterimagePass );

        var o = 1;

        function animate() {
            requestAnimationFrame( animate );
            const dt = clock.getDelta();
            plain.material.uniforms.time.value = t * 50;
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
            //moveBall();
            checkCollision();
            if (o == 1)
            {
                renderer.render( scene, camera );
            }
        }
        animate(); })();
    });
</script>

<canvas bind:this={canvas} class=""></canvas>