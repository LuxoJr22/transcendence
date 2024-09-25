import * as THREE from 'three';

export function createmap(scene)
{
	var texture = new THREE.TextureLoader().load( 'src/routes/shooter/public/images.jpg' );
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
}