import * as THREE from 'three';

interface Dictionary<T> {
	[Key: string]: T;
}

export class Player {
	mesh : THREE.Object3D;
	left : THREE.Object3D;
	right : THREE.Object3D;
	bone : THREE.Object3D;

	ySpeed : number;
	xSpeed : number;
	side : number;
	
	gamepad = 0;
	point = 0;
	dir = 0;
	animleg = 0
	canmove = 1;
	charging = 1;
	knockback = 0;
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
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
	
		this.limit = limit;
		this.bind = bind;
	}
	update () {
		this.knockback = THREE.MathUtils.lerp(this.knockback, 0, 0.1)
		this.action();

		this.movelegs()
	}
	movelegs()
	{
		let diry = (this.controllanims.yn + this.controllanims.yp) * this.side;
		let dirx = (this.controllanims.xn + this.controllanims.xp) * this.side;

		if (dirx != 0)
			this.dir = Math.atan(diry / dirx);
		else
			this.dir = Math.asin(diry * 10 * 2/3);
		if (this.charge == 0)
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
		else
		{
			this.bone.rotation.y = 0
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
			this.bone.rotation.x = THREE.MathUtils.lerp(this.bone.rotation.x , -Math.PI / 2 , 0.5)
		}
	}
	keydown (keyCode : number) {
		if (keyCode == this.bind.up)
			this.controller.yp = this.ySpeed;
		if (keyCode == this.bind.down)
			this.controller.yn = -this.ySpeed;
		if (keyCode == this.bind.left)
			this.controller.xn = -this.xSpeed;
		if (keyCode == this.bind.right)
			this.controller.xp = this.xSpeed;
		if (keyCode == this.bind.charge)
		{
			this.controller.charge = 1;
		}
	}
	keyup (keyCode : number) {
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
		if (this.controllanims.charge == 1 && this.charge == 0)
		{
			this.animleg = -Math.PI / 2;
			this.left.rotation.z = -Math.PI / 2;
			this.right.rotation.z = Math.PI / 2;
			this.left.rotation.y = 0;
			this.right.rotation.y = 0;
			this.left.rotation.x = 0;
			this.right.rotation.x = 0;
			this.charge = 1;
		}
		if (this.controllanims.charge == 0 && this.charge)
		{
			this.charge = 0;
			this.knockback = this.charging / 10;
			this.bone.rotation.x = 0;
		}
	}
}