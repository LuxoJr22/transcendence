<script lang="ts">
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
	import { auth, fetchUser } from '$lib/stores/auth';
	import type { AuthState } from '$lib/stores/auth';
	
    let canvas : HTMLCanvasElement;
	let state: AuthState;
	$: $auth, state = $auth;

	onMount(() => { (async () => {
		await fetchUser()
		auth.subscribe((value : AuthState) =>{
            state = value;
        });
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera( 90, 2, 0.1, 1000 );
		scene.background = new THREE.Color(0x111111);
		var hit = 0

		var canvasSize = {width: window.innerWidth * 0.7,  height: window.innerWidth * 0.7 / 2 * 1}
		var t = 0;
		const clock = new THREE.Clock();
		const loader = new GLTFLoader()
		const skin = await loader.loadAsync('/src/lib/assets/skins/gilles.glb');
        var rotating_skin = skin.scene;
		rotating_skin.scale.set(0.3, 0.3, 0.3);
		scene.add(rotating_skin)

		const light = new THREE.AmbientLight(0xffffff, 1.5)
		scene.add(light)
		const dl = new THREE.DirectionalLight( 0xffffff, 1.5);
		dl.position.set( 0, 0.8, 1.7 );
		scene.add( dl );
		
		const renderer = new THREE.WebGLRenderer({canvas, antialias: false});
		renderer.setSize( canvasSize.width, canvasSize.height);
		renderer.shadowMap.enabled = true;

		var def_gloves = [document.getElementById("left_def"), document.getElementById("right_def")]

		var att_gloves = [document.getElementById("left_att"), document.getElementById("right_att")]


		var top = renderer.domElement.getBoundingClientRect().top
		var	l = renderer.domElement.getBoundingClientRect().left

		camera.position.x = 0;
		camera.position.y = 0.8;
		camera.position.z = 1.7;

		var gloves = document.getElementById("gloves_ui");

		var ui = document.getElementById("ui");
		ui!.style.width = canvasSize.width + "px";
		ui!.style.height = canvasSize.height + "px";

		window.onresize = function(event){
			canvasSize.width = window.innerWidth * 0.7
			canvasSize.height = window.innerWidth * 0.7 / 2 * 1
			ui!.style.width = canvasSize.width + "px";
       		ui!.style.height = canvasSize.height + "px";
			top = renderer.domElement.getBoundingClientRect().top
			l = renderer.domElement.getBoundingClientRect().left
			renderer.setSize( canvasSize.width, canvasSize.height);
		}


		


		var left = rotating_skin.getObjectByName("Bone003L");
		var right = rotating_skin.getObjectByName("Bone003R");
		var bone = rotating_skin.getObjectByName("Bone");
		var animleg = 0;
		var dir = 0
		var dirx = 0
		var diry = 0


		const raycaster = new THREE.Raycaster()
		const clickmouse = new THREE.Vector2()

		

		window.addEventListener('click', async(event) => {
			clickmouse.x = ((event.clientX - l) / renderer.domElement.clientWidth) * 2 - 1
			clickmouse.y = -(((event.clientY - top) / renderer.domElement.clientHeight) * 2 - 1)
			
			if (hit <= 0)
			{
				
				if (clickmouse.x < 0)
				{
					att_gloves[1]!.style.display = "none"
					att_gloves[0]!.style.display = "flex"
					att_gloves[0]!.style.top = (event.clientY - top) + "px"
					att_gloves[0]!.style.left = (event.clientX - l) + "px"
					def_gloves[0]!.style.visibility = "hidden"
					def_gloves[1]!.style.visibility = "visible"
				}
				else {
					att_gloves[0]!.style.display = "none"
					att_gloves[1]!.style.display = "flex"
					att_gloves[1]!.style.top = (event.clientY - top) + "px"
					att_gloves[1]!.style.left = (event.clientX - l) + "px"
					def_gloves[1]!.style.visibility = "hidden"
					def_gloves[0]!.style.visibility = "visible"
				}
				raycaster.setFromCamera( clickmouse, camera)
				const found = raycaster.intersectObjects(scene.children);
				if (found[0])
				{
					if (clickmouse.x < 0)
						hit_pose(-1)
					else
						hit_pose(1)
					hit = 0.5;
					var sphere = new THREE.Mesh(new THREE.SphereGeometry(0.15 , 5, 5), new THREE.MeshBasicMaterial( { color: 0xffcccc} ))
					sphere.position.set(found[0].point.x, found[0].point.y ,found[0].point.z );
					//rotating_skin.attach(sphere)
					//bone.attach(sphere)
					//sphere.applyMatrix4(new THREE.Matrix4(sphere.Matrix4));
				}
			}
		});

		var face : THREE.Object3D[] = []
		var skinned : THREE.Object3D
		rotating_skin.traverse(function(node : THREE.Object3D) {
			if (node.isMesh)
			{
				node.castShadow = true;
				node.receiveShadow = true;
				if (!node.isSkinnedMesh)
					face.push(node)
				else
					skinned = node
			}
		})

		// var box = new THREE.Box3().setFromObject(rotating_skin);
		// var size = new THREE.Vector3();
		// box.getSize(size);
		// rotating_skin.children[0].children[0].material = new THREE.MeshBasicMaterial({color: 0xffddff, skinning: true});
		// rotating_skin.children[0].children[0].material.color.set(0xffffff);
		// rotating_skin.children[0].children[0].material.onBeforeCompile = function ( shader ) {
		// 	shader.uniforms.time = { value: 0 };
		// 	shader.uniforms.size = { value: size};
		// 	shader.uniforms.color1 = {value: new THREE.Color(0xff00ff)};
		// 	shader.uniforms.color2 = {value: new THREE.Color(0xffff00)};
		// 	shader.vertexShader = 'varying vec4 vWorldPosition;\n' + shader.vertexShader;
		// 	shader.vertexShader = shader.vertexShader.replace(
		// 	'#include <worldpos_vertex>',
		// 	[
		// 		'#include <worldpos_vertex>',
		// 		'vWorldPosition = modelMatrix * vec4( transformed, 1.0 );'
		// 	].join( '\n' )
		// 	);
		// 	shader.fragmentShader = 'uniform float time;\nuniform vec3 size;\nuniform vec3 color1;\nuniform vec3 color2;\nvarying vec4 vWorldPosition;\n' + shader.fragmentShader;
		// 	// shader.fragmentShader = shader.fragmentShader.replace(
		// 	// '#include <map_fragment>',
		// 	// [
		// 	// 	'#include <map_fragment>',
		// 	// 	'vec4 sampledDiffuseColor = texture2D( map, vMapUv );',
		// 	// 	'diffuseColor *= sampledDiffuseColor;',
		// 	// ].join( '\n' )
		// 	// );
		// 	shader.fragmentShader = shader.fragmentShader.replace(
		// 	'#include <dithering_fragment>',
		// 	[
		// 		'#include <dithering_fragment>',
		// 		'float gridRatio = sin( time ) * 0.1875 + 0.3125;', // 0.125 .. 0.5
		// 		'vec3 m = abs( sin( vWorldPosition.xyz * gridRatio ) );',
		// 		'vec3 gridColor = mix(color1, color2, vWorldPosition.y / size.y);',
				
		// 		'gl_FragColor = vec4( mix( gridColor, diffuseColor.rgb, m.x * m.y * m.z ), diffuseColor.a );',
		// 		// 'diffuseColor = vec4( mix( gridColor, diffuseColor.rgb, m.x * m.y * m.z ), diffuseColor.a );',
		// 	].join( '\n' )
		// 	);

		// 	rotating_skin.ShaderMaterial = shader
		// };




		function hit_pose(sign : number)
		{
			// left.rotation.set(0, 0, THREE.MathUtils.lerp(left.rotation.z, -Math.PI / 6, 0.1))
			// right.rotation.set(0, 0, THREE.MathUtils.lerp(right.rotation.z, Math.PI / 6, 0.1))
			// bone.rotation.set(THREE.MathUtils.lerp(bone.rotation.x, -Math.PI / 6, 0.1), 0, 0)

			rotating_skin.rotation.set(0, Math.PI / 6 * sign, 0)
			face.forEach( (e) => {
				// e.scale.set(0.3, 0.5, 1)
				e.scale.set(0.6, 0.3, 1)
			})
			left.rotation.set(0, 0, -Math.PI / 6)
			right.rotation.set(0, 0, Math.PI / 6)
			bone.rotation.set(-Math.PI / 6, 0, 0)
		}

		function reset_pose(){
			rotating_skin.rotation.set(0, 0, 0)
			face.forEach( (e) => {
				e.scale.set(1, 1, 1)
			})
			left.rotation.set(0, 0, 0)
			right.rotation.set(0, 0, 0)
			bone.rotation.set(0, 0, 0)
		}

		function animateLegs(time : number) {

			if (dirx != 0)
				dir = Math.atan(diry / dirx);
			else
				dir = Math.asin(diry * 10 * 2 / 3);
			
			if (dirx == 0 && diry == 0)
				animleg = 0;
			else if (animleg == 0)
				animleg = Math.PI / 3;
			if (animleg != 0 && Math.abs(left.rotation.z) >= Math.abs(animleg) - 0.2)
				animleg *= -1;

			left.rotation.y = -dir;
			right.rotation.y = -dir;
			left.rotation.x = 0;
			right.rotation.x = 0;
			left.rotation.z = THREE.MathUtils.lerp(left.rotation.z, animleg, 0.1);
			right.rotation.z = THREE.MathUtils.lerp(right.rotation.z, animleg, 0.1);
			//bone.rotation.y = THREE.MathUtils.lerp(bone.rotation.y, dir / 8, 0.2);
			if (dirx < 0)
				dirx = 0;
			bone.rotation.x = THREE.MathUtils.lerp(bone.rotation.x, animleg / 10 + -dirx * 2, 0.1);
		}

		function animate() {
			requestAnimationFrame( animate );
			const dt = clock.getDelta();
			t += dt;
			if (hit > 0)
			{
				hit -= dt;
				if (hit <= 0){
					reset_pose()
					att_gloves[1]!.style.display = "none"
					att_gloves[0]!.style.display = "none"
					def_gloves[1]!.style.visibility = "visible"
					def_gloves[0]!.style.visibility = "visible"
				}	
			}
			renderer.render( scene, camera );
		}
		animate();
	})();
	});
</script>

<style>
	#ui {
        position: absolute;
		pointer-events: none;
		width: 10px;
		height: 10px;
		overflow: hidden;
    }

	#gloves {
		display: flex;
		justify-content: center;
		pointer-events: none;
		transform: translate(-50%);	
	}


	.glove {
		height: 300px;
		pointer-events: none;
		
	}

	#gloves_ui {
		position: absolute;
		display: flex;
		pointer-events: none;
		left: 50%;
		bottom: 0%;
	}

	#att_gloves_ui {
		position: absolute;
		display: inline;
		pointer-events: none;
		width: 100%;
		height: 100%;
		bottom: 0%;
	}

	.att_glove {
		display: none;
		position: absolute;
		pointer-events: none;
		bottom: 0;
  		right: 0;
		transform: translate(-50%, -50%);	
	}

</style>

<div id="ui">
	<div id=gloves_ui>
		<div id="gloves">
			<img alt="left_def_glove" class="glove" id="left_def" src="/src/lib/assets/left_def_glove.png"/>
			<img alt="right_def_glove" class="glove" id="right_def" src="/src/lib/assets/right_def_glove.png"/>
		</div>
	</div>
	<div id=att_gloves_ui>
		<img alt="left_att_glove" class="att_glove" id="left_att" src="/src/lib/assets/left_att_glove.png"/>
		<img alt="right_att_glove" class="att_glove" id="right_att" src="/src/lib/assets/right_att_glove.png"/>
	</div>
</div>

<canvas bind:this={canvas} class=""></canvas>

