<script lang= "ts">
    import { onMount } from 'svelte';
    import { GUI } from 'three/addons/libs/lil-gui.module.min.js';
    import * as THREE from 'three';
    import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
    import { Shooter } from "./shooter.js";
    import { Player } from "./player.js";
    import { flagshader } from "./flagshader";

    let canvas;
    var scoring = 0;
    export var ls = 0;

    onMount(() => { (async () => {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.1, 1000 );
        camera.position.z = 30;
        camera.position.y = 10;

        let t = 0;
        const clock = new THREE.Clock();
        var reload = 0;

        var el = document.getElementById("blocker");
        var ui = document.getElementById("ui");
        var circle = document.getElementById("circular");
        var ficon = document.getElementById("flagicon");


        scene.background = new THREE.Color(0x54A0E4);

        var flagposs = 0;

        
        var bind2 = {up: 90, down: 83, left:81, right:68, jump:32}
        var bind = {up: 40, down: 38, left:39, right:37, jump:96}

        var texture = new THREE.TextureLoader().load( 'src/routes/game2/public/images.jpg' );
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        texture.repeat.set( 4, 4 );

        var mat = new THREE.MeshStandardMaterial( { map : texture})

        
        const box = new THREE.Mesh(new THREE.BoxGeometry(100, 1, 1), new THREE.MeshStandardMaterial( { color: 0xffffff }))
        box.castShadow = true;
        scene.add(box)

        const bbox = new THREE.Mesh(new THREE.BoxGeometry(15, 10, 15), mat)
        bbox.position.set(0, 0, -5)
        bbox.castShadow = true;
        scene.add(bbox)


        /*********************************************************************************************************************/
        /***************************************************  TEST **********************************************************/
        /*********************************************************************************************************************/
        class SkeletonCollider {
            distance = 0
            v1 = new THREE.Vector3()
            v2 = new THREE.Vector3()
            bones = []
            material = new THREE.MeshBasicMaterial({
                color: 0xff0000,
                wireframe: true,
                depthTest: false,
            })
            constructor(object) {
                object.traverse((child) => {
                    if (child.isBone) {
                        if (child.parent && child.parent.type === 'Bone') {
                            this.bones.push(child)
                            child.getWorldPosition(this.v1)
                            child.parent.getWorldPosition(this.v2)
                            this.distance = this.v2.distanceTo(this.v1)
                            let g
                            switch (child.name) {
                                case 'Bone001':
                                {
                                    g = new THREE.BoxGeometry(3, 1, 1)
                                    g.translate(0, this.distance / 2 - 0.3, 0)
                                    break;
                                }
                                default:
                                {
                                    g = new THREE.BoxGeometry(0.2, this.distance, 0.2)
                                    g.translate(0, this.distance / 2, 0)
                                    break
                                }
                            }
                            
                            const m = new THREE.Mesh(g, this.material)
                            m.visible = false
                            scene.add(m)

                            child.userData.m = m
                            pickables.push(m)
                        }
                    }
                })
            }

            update() {
                this.bones.forEach((b) => {
                    b.getWorldPosition(b.userData.m.position)
                    b.getWorldQuaternion(b.userData.m.quaternion)
                })
            }
        }


        /*********************************************************************************************************************/
        /***************************************************  TEST **********************************************************/
        /*********************************************************************************************************************/

        const plain = new THREE.Mesh(new THREE.PlaneGeometry(300, 100), mat);

        plain.position.set(0, -1, 0);
        plain.rotation.x = -Math.PI / 2
        //plain.overdraw = true;
        plain.receiveShadow = true;

        scene.add(plain);

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

        var collider = [new THREE.Box3().setFromObject( box), new THREE.Box3().setFromObject( bbox)];

        //#region LoadModel

        const loader = new GLTFLoader()

        const flag = await loader.loadAsync('src/routes/game2/public/f.glb');
        const fb = new THREE.Mesh(new THREE.BoxGeometry(15, 5, 15), new THREE.MeshStandardMaterial( { color: 0xff0000 }));
        fb.position.set(0, 7.5, -5);
        const fbb = new THREE.Box3().setFromObject(fb)

        flag.scene.position.set(0, 5, -5);

        scene.add(flag.scene);

        /*const mount = await loader.loadAsync('src/routes/game2/public/mountain.glb');
        mount.scene.scale.set(10, 10, 10);
        scene.add(mount.scene);*/

        var collider = [new THREE.Box3().setFromObject( box), new THREE.Box3().setFromObject( bbox)/*, new THREE.Box3().setFromObject( mount.scene)*/];

        
        const gl = await loader.loadAsync('src/routes/game2/public/sty.glb');

        gl.scene.position.set(10, 0, -1.5);
        gl.scene.scale.set(0.5, 0.5, 0.5);

        var er = new Player(gl, bind, 0.15, 0);
        er.mesh.traverse(function(node) {
            if (node.isMesh)
                node.castShadow = true;
        })
        scene.add(er.mesh);

        const pickables = [];
        let skeletonCollider = new SkeletonCollider(er.mesh)


        const gltf = await loader.loadAsync('src/routes/game2/public/pop.glb');


        gltf.scene.position.set(0, 0.5, 3);
        gltf.scene.scale.set(0.5, 0.5, 0.5);

        var play = new Shooter(gltf, bind2, 0.15, camera, scene, er.mesh, collider, pickables);
        //scene.add(play.mesh);

        el.addEventListener('click', function () {
            el.style.display = "none";
            play.cam.lock();
        });


        play.cam.addEventListener( 'unlock', function () {
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
        renderer.setSize( 1920 * 0.7 , 1080 * 0.7);
        ui.style.width = 1920 * 0.7 + "px";
        ui.style.height = 1080 * 0.7 + "px";
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
            if (event.which == 1 && reload == 0)
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
                        er.mesh.position.set(Math.random() * 20, Math.random() * 2, Math.random() * 10)
                }
            }
            if (event.which == 3)
            {
                var intersects = play.raycaster.intersectObjects( scene.children );
                let i = 0
                if (intersects[i] && intersects[ i ].object == play.bb)
                    i ++;
                if (intersects[i] && intersects[ i ].object != play.sphere)
                {
                    play.sphere.position.set(intersects[i].point.x, intersects[i].point.y ,intersects[i].point.z );
                    if (play.bbox.intersectsSphere(play.spherebb))
                    {
                        play.velocity.y += (10 - intersects[ i ].distance);
                        play.velocity.x += 10;
                    }
                }
            }
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

        

        function CheckCollision(dt)
        {
            if (play.bbox.intersectsBox(fbb))
                flagposs += dt;
        }

        function animate() {
            requestAnimationFrame( animate );
            const dt = clock.getDelta();
            if (flagposs >= 5)
            {
                ficon.style.display = "block";
                scene.remove(flag.scene);
                if (Math.tan(sh.material.uniforms.time.value) > 2.0)
                    scene.remove(sh)
                if (Math.tan(tor.material.uniforms.time.value) > 2.0)
                    scene.remove(tor)
                if (Math.tan(toru.material.uniforms.time.value) > 2.0)
                    scene.remove(toru)
            }
            t += dt;
            if (gamepads[0])
            {
                gamepads[0] = navigator.getGamepads()[0]
                handlebuttons(gamepads[0].buttons)
                handlesticks(gamepads[0].axes)
            }
            if (reload > 0)
            {
                reload -= dt * 250;
                circle.style.background = `conic-gradient(#cccccc ${360 - reload}deg, rgba(1.0, 1.0, 1.0, 0.0) 0deg)`
            }
            else
            {
                reload = 0;
                circle.style.background = `conic-gradient(#cccccc 0deg, rgba(1.0, 1.0, 1.0, 0.0) 0deg)`
            }
            CheckCollision(dt);
            skeletonCollider.update()
            play.update(dt)
            er.update(dt)
            sh.material.uniforms.time.value = t;
            tor.material.uniforms.time.value = t + 1;
            toru.material.uniforms.time.value = t + 2;
            renderer.render( scene, camera );
        }
        animate(); 
    })();
    });
</script>

<style>
    #ui {
        position: absolute;
		width: 10px;
		height: 10px;
    }
    #blocker {
				position: absolute;
				width: 100%;
				height: 100%;
				background-color: rgba(0,0,0,0.1);
			}
    #crosshair {
        position: absolute;
        top: 50%;
        left: 50%;
        z-index: 1;
        pointer-events: none;
    }
    #crossimg {
        width: 50%;
        position: relative;
        top: -100px;
        left: -100px;
    }

    #circular {
        position: absolute;
        width: 30px;
        height: 30px;
        top: -15px;
        left: -15px;
        border-radius: 50%;
        background: conic-gradient(#cccccc 0deg, rgba(1.0, 1.0, 1.0, 0.0) 0deg);
    }

    #flagicon {
        display: none;
    }


</style>

<div id="ui">
    <div id="blocker">
    </div>
    <div>
        <img id="flagicon" src="src/routes/game2/public/flag.png"/>
    </div>
    <div id="crosshair">
        <div id="circular"></div>
        <img id="crossimg" src="src/routes/game2/public/dotcrosshair.png"/>
    </div>
</div>

<canvas bind:this={canvas} class=""></canvas>