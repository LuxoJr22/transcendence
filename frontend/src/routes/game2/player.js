import * as THREE from 'three';

export class Player {
	constructor (mesh, bind, speed, cam) {
		this.ySpeed = speed * 2;
		this.cam = cam;
		this.xSpeed = speed * 2;
		this.mesh = mesh.scene;
		this.bb = new THREE.Box3().setFromObject( mesh.scene);
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
		this.raycaster = new THREE.Raycaster( new THREE.Vector3(), new THREE.Vector3( 0, - 1, 0 ), 0, 10 );
		this.gamepad = 0;
		this.point = 0;
		this.dir = 0;

		this.animleg = 0

		this.canmove = 1;
		this.isfalling = 0;
		this.knockback = 0;
		this.direction = new THREE.Vector3();
	
		this.bind = bind;

		this.controller = {xp: 0, xn: 0, yp: 0, yn: 0, jump: 0}
	}
	update (dt) {
		/*this.raycaster.ray.origin.copy( this.cam.getObject().position );
		this.raycaster.ray.origin.y -= 10;
		let onobj = this.raycaster.intersectObjects( ob)*/
		let d = Math.acos(this.direction.x)
		if (this.direction.z < 0)
			d *= -1;
		this.mesh.rotation.y = -d + Math.PI / 2;
		this.knockback = THREE.MathUtils.lerp(this.knockback, 0, 0.1)
		this.action();
		if (this.canmove)
			this.move();
	}
	movelegs()
	{
		let diry = this.controller.yn + this.controller.yp;
		let dirx = this.controller.xn + this.controller.xp;

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
	move () {
		this.movelegs();
		let ym, xm;
		this.bb = new THREE.Box3().setFromObject(this.mesh);
		xm = this.controller.xn + this.controller.xp + this.knockback;
		ym = this.controller.yn + this.controller.yp;
		this.mesh.translateX(xm);
		this.mesh.translateZ(ym);
		if (this.cam)
		{
			this.cam.moveForward(ym);
			this.cam.moveRight(xm);
		}
	}
	keydown (keyCode) {
		if (keyCode == this.bind.up)
			this.controller.yp = this.ySpeed;
		if (keyCode == this.bind.down)
			this.controller.yn = -this.ySpeed;
		if (keyCode == this.bind.left)
			this.controller.xn = -this.xSpeed;
		if (keyCode == this.bind.right)
			this.controller.xp = this.xSpeed;
		if (keyCode == this.bind.jump)
		{
			this.controller.jump = 1;
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

		if (keyCode == this.bind.jump)
		{
			this.controller.jump = 0;
		}
	}
	action() {
	}
}