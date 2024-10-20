import * as THREE from 'three';

interface Dictionary<T> {
	[Key: string]: T;
}

export class Player {
	bb : THREE.Box3;
	mesh : THREE.Object3D;
	left : THREE.Object3D;
	right : THREE.Object3D;
	bone : THREE.Object3D;

	ySpeed : number;
	xSpeed : number;
	side : number;
	
	gamepad = 0;
	dir = 0;
	animleg = 0
	charge = 0;

	limit : Dictionary<number>;
	bind :  Dictionary<number>;

	controller = {xp: 0, xn: 0, yp: 0, yn: 0, charge: 0}
	controllanims = {xp: 0, xn: 0, yp: 0, yn: 0, charge: 0}

	constructor (mesh : THREE.Object3D, bind : Dictionary<number>, limit : Dictionary<number>, speed : number, side : number) {
		this.ySpeed = speed;
		this.xSpeed = speed;
		this.mesh = mesh.scene;
		this.side = side;
		this.bb = new THREE.Box3().setFromObject( mesh.scene);
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
	
		this.limit = limit;
		this.bind = bind;

	}
	movelegs()
	{
		let diry = (this.controllanims.yn + this.controllanims.yp) * this.side;
		let dirx = (this.controllanims.xn + this.controllanims.xp) * this.side;

		if (dirx != 0)
			this.dir = Math.atan(diry / dirx);
		else
			this.dir = Math.asin(diry * 10 * 2/3);

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
	keydown (keyCode : number) {
		if (keyCode == this.bind.up)
			this.controller.yp = this.ySpeed;
		if (keyCode == this.bind.down)
			this.controller.yn = -this.ySpeed;
	}
	keyup (keyCode : number) {
		if (keyCode == this.bind.up)
			this.controller.yp = 0;
		if (keyCode == this.bind.down)
			this.controller.yn = 0;
	}
}