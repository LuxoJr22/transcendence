import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export async function createmap(scene, loader)
{
	var texture = new THREE.TextureLoader().load( 'src/routes/(private)/shooter/public/images.jpg' );
	texture.wrapS = THREE.RepeatWrapping;
	texture.wrapT = THREE.RepeatWrapping;
	texture.repeat.set( 4, 4 );

	var mat = new THREE.MeshStandardMaterial( { map : texture})

	const bbox = new THREE.Mesh(new THREE.BoxGeometry(15, 10, 15), mat)
	bbox.position.set(0, 0, -5)
	bbox.castShadow = true;
	scene.add(bbox)


	const plain = new THREE.Mesh(new THREE.PlaneGeometry(300, 100), mat);
    plain.position.set(0, -1, 0);
    plain.rotation.x = -Math.PI / 2
    //plain.overdraw = true;
    plain.receiveShadow = true;
    scene.add(plain);
	

	const map = await loader.loadAsync('src/lib/assets/maps/shooter/map.glb');
	map.scene.rotation.y = Math.PI / 2
	map.scene.scale.set(8, 8, 8)
	scene.add(map.scene);


	const amblight = new THREE.AmbientLight( 0xffffff, 0.1 );
	scene.add( amblight );

	const dl = new THREE.DirectionalLight( 0xffffff, 0.1 );
	
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

	
}