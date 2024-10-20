import * as THREE from 'three';
import { SkeletonCollider } from "./skeletoncollider"

export class Player {
	ySpeed : number;
	xSpeed : number;
	id : number;
	scene : THREE.Scene;
	mesh : THREE.Object3D;
	skeletonCollider : SkeletonCollider;
	bb : THREE.Box3;
	left : THREE.Object3D;
	right : THREE.Object3D;
	bone : THREE.Object3D;
	raycaster = new THREE.Raycaster( new THREE.Vector3(), new THREE.Vector3( 0, - 1, 0 ), 0, 10 );
	gamepad = 0;
	point = 0;
	dir = 0;
	grounded = 1;

	footdir = new THREE.Vector3(0, -1 ,0)
	foot = new THREE.Raycaster();

	animleg = 0

	canmove = 1;
	isfalling = 0;
	direction = new THREE.Vector3();

	target : THREE.Object3D[];

	controller = {xp: 0, xn: 0, yp: 0, yn: 0, jump: 0}

	constructor (mesh : THREE.Object3D, speed : number, scene : THREE.Scene, id : number) {
		this.ySpeed = speed * 2;
		this.xSpeed = speed * 2;
		this.id = id
		this.scene = scene;
		this.mesh = mesh.scene;
		this.mesh.traverse(function(node : THREE.Object3D) {
            if (node.isMesh)
                node.castShadow = true;
            if (node.isSkinnedMesh)
                node.frustumCulled = false;
        })
		const pickables : THREE.Object3D[] = [];
        this.skeletonCollider = new SkeletonCollider(this.mesh, this.scene, pickables)
        this.scene.add(this.mesh);
		this.bb = new THREE.Box3().setFromObject( mesh.scene);
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
		this.foot.far = 2

		this.target = this.mesh.getObjectByName("Bone001").children;
		this.target = this.target.concat(pickables)
		this.target.forEach(function(element) {
			element.userData.id = id
		}, id)


		this.controller = {xp: 0, xn: 0, yp: 0, yn: 0, jump: 0}
	}
	update (dt : number) {
		this.skeletonCollider.update()
		this.foot.set(new THREE.Vector3(this.mesh.position.x, this.mesh.position.y + 1 ,this.mesh.position.z), this.footdir)
		var inter = this.foot.intersectObjects( this.scene.children );
		
		var i = 0
		
		if (inter[i])
		{
			if (this.target.includes(inter[i].object))
				i++
			if (inter[i])
			{
				this.grounded = 1;
			}
			else
				this.grounded = 0;
		}
		else
			this.grounded = 0;
		this.movelegs();
	}
	movelegs()
	{
		let dirx = (this.controller.yn + this.controller.yp) / 2;
		let diry = (this.controller.xn + this.controller.xp) / 2;

		if (dirx != 0)
			this.dir = Math.atan(diry / dirx);
		else
			this.dir = Math.asin(diry * 10 * 2/3);

		if (this.grounded)
		{
			if (dirx == 0 && diry == 0)
				this.animleg = 0;
			else if (this.animleg == 0)
				this.animleg = Math.PI / 3;
			if (this.animleg != 0 && Math.abs(this.left.rotation.z) >= Math.abs(this.animleg) - 0.2)
				this.animleg *= -1;
			this.left.rotation.y = -this.dir;
			this.right.rotation.y = -this.dir;
			this.left.rotation.x = 0;
			this.right.rotation.x = 0;
			this.left.rotation.z = THREE.MathUtils.lerp(this.left.rotation.z, this.animleg, 0.1);
			this.right.rotation.z = THREE.MathUtils.lerp(this.right.rotation.z, this.animleg, 0.1);
			this.bone.rotation.y = THREE.MathUtils.lerp(this.bone.rotation.y, this.dir / 8, 0.2);
			if (dirx < 0)
				dirx = 0;
			this.bone.rotation.x = THREE.MathUtils.lerp(this.bone.rotation.x, this.animleg / 10 + -dirx * 2, 0.1);
		}
		else if (!this.grounded)
		{
			this.animleg = 0
			if (this.animleg == 0 && (dirx < 0))
				this.animleg = Math.PI / 3;
			else if (this.animleg == 0 && (dirx > 0))
				this.animleg = -Math.PI / 3;
			else if (diry != 0)
				this.animleg = -Math.PI / 3;
			this.left.rotation.y = -this.dir;
			this.right.rotation.y = -this.dir;
			this.left.rotation.z = THREE.MathUtils.lerp(this.left.rotation.z, this.animleg, 0.1);
			this.right.rotation.z = THREE.MathUtils.lerp(this.right.rotation.z, -this.animleg, 0.1);
		}
	}
}