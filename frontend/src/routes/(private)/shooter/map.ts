import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export async function createmap(scene : THREE.Object3D, loader : GLTFLoader)
{
	const map = await loader.loadAsync('src/lib/assets/maps/shooter/map.glb');
	map.scene.rotation.y = Math.PI / 2
	map.scene.scale.set(8, 8, 8)

	map.scene.castShadow = true;
	map.scene.receiveShadow = true;
	map.scene.traverse( function( child : THREE.Object3D ) { 

		if ( child.isMesh ) {
	
			child.castShadow = true;
			child.receiveShadow = true;
	
		}
	
	} );

	scene.add(map.scene);

	const hemlight = new THREE.HemisphereLight(0xffffff, 0x080820, 1);
	scene.add( hemlight );

	const amblight = new THREE.AmbientLight( 0xffffff, 0.5 );
	scene.add( amblight );

	const dl = new THREE.DirectionalLight( 0xffffff, 0.5 );
	
	dl.position.set( -30, 100, 0 );
	dl.target.position.set(0, 0, 0)
	dl.castShadow = true;
	scene.add( dl );
	scene.add( dl.target)


	var size = 70;
	dl.shadow.camera.top = size;
	dl.shadow.camera.bottom = -size;
	dl.shadow.camera.left = size;
	dl.shadow.camera.right = -size;
	dl.shadow.camera.near = 25;
	dl.shadow.camera.far = 250;
    dl.shadow.bias = -0.008;

	const dl1 = new THREE.DirectionalLight( 0xffffff, 0.2 );
	
	dl1.position.set( 30, 100,  );
	dl1.target.position.set(0, 0, 0)
	scene.add( dl1 );
	scene.add( dl1.target)

	var shadowCameraHelper = new THREE.CameraHelper(dl.shadow.camera);
	shadowCameraHelper.visible = true;

	
}