<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as THREE from 'three';
	import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
	import { profileData, profile, type Profile } from '$lib/stores/user';
	import { auth, fetchUser } from '$lib/stores/auth';
	import type { AuthState } from '$lib/stores/auth';
	
    let canvas : HTMLCanvasElement;
	let state: AuthState;
	let user : Profile;
	let isLoad : boolean = false;

	let users = []
    $: user = $profile;

	$: $auth, state = $auth;

	onMount(() => { (async () => {
		await fetchUser()
		auth.subscribe((value : AuthState) =>{
            state = value;
        });
		isLoad = true

		
        const response = await fetch("/api/pong/history/" + state.user?.id, {
            method: 'GET',
            headers:{
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            }
        });

        if (response.ok) {
            var historyData = await response.json();
        }
		
		let i = 0;
		while (historyData[i])
		{
			console.log(historyData[i].winner)
			if (historyData[i].winner != state.user!.id)
			{
				await profileData(parseInt(historyData[i].winner));
				profile.subscribe((value : Profile) =>{
					user = value;
				})
				users.push(user)
			}
			i++
		};

		var nb_hit = 0

		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera( 90, 2, 0.1, 1000 );
		scene.background = new THREE.Color(0x212529);
		var hit = 0

		var canvasSize = {width: window.innerWidth * 0.7,  height: window.innerWidth * 0.7 / 2 * 1}
		var t = 0;
		const clock = new THREE.Clock();
		const loader = new GLTFLoader()
		if (users[0])
			var skin = await loader.loadAsync('/assets/skins/' + users[0].skin);
		else
			var skin = await loader.loadAsync('/assets/skins/gilles.glb');
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
		camera.position.y = 0.9;
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


		
		const ring = await loader.loadAsync('/assets/maps/waiting/boxing_ring.glb');
		ring.scene.position.set(0, -3, 0)

		scene.add(ring.scene)

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
					
					hit = 0.5;
					var sphere = new THREE.Mesh(new THREE.SphereGeometry(0.1 , 5, 5), new THREE.MeshBasicMaterial( { color: 0xffcccc} ))
					sphere.scale.z = 0.5
					sphere.position.set(found[0].point.x, found[0].point.y ,found[0].point.z );
					bone.attach(sphere)
					nb_hit ++;
					if (clickmouse.x < 0)
						hit_pose(-1)
					else
						hit_pose(1)
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
			if (isLoad)
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

	onDestroy(() => {
		isLoad = false;
	})

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
			<img alt="left_def_glove" class="glove" id="left_def" src="/assets/ui/waiting/left_def_glove.png"/>
			<img alt="right_def_glove" class="glove" id="right_def" src="/assets/ui/waiting/right_def_glove.png"/>
		</div>
	</div>
	<div id=att_gloves_ui>
		<img alt="left_att_glove" class="att_glove" id="left_att" src="/assets/ui/waiting/left_att_glove.png"/>
		<img alt="right_att_glove" class="att_glove" id="right_att" src="/assets/ui/waiting/right_att_glove.png"/>
	</div>
</div>

<canvas bind:this={canvas} class=""></canvas>

