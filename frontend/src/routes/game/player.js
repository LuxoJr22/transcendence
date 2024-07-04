import * as THREE from 'three';

export class Player {
	constructor (mesh, bind, limit, speed) {
		this.ySpeed = speed;
		this.xSpeed = speed;
		this.mesh = mesh.scene;
		this.mixer = new THREE.AnimationMixer( mesh.scene );
		this.bb = new THREE.Box3().setFromObject( mesh.scene);
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
		this.gamepad = 0;
		this.point = 0;
		this.dir = 0;

		this.animleg = 0

		this.canmove = 1;
		this.isfalling = 0;
		this.charging = 1;
		this.knockback = 0;
	
		this.limit = limit;
		this.bind = bind;
		let load = this.mixer.clipAction( mesh.animations[ 1 ] );
		let fall = this.mixer.clipAction( mesh.animations[ 2 ] );
		load.setLoop(THREE.LoopOnce);
		load.clampWhenFinished = true;
		fall.setLoop(THREE.LoopOnce);
		this.anims = {load: load, fall: fall};
		this.charge = 0;

		this.controller = {xp: 0, xn: 0, yp: 0, yn: 0, charge: 0}
	}
	update (dt) {
		this.knockback = THREE.MathUtils.lerp(this.knockback, 0, 0.1)
		this.action();
		if (this.charge && this.anims.load.time < 0.1 && !this.isfalling)
		{
			this.animleg = -Math.PI / 2;
			this.left.rotation.z = -Math.PI / 2;
			this.right.rotation.z = Math.PI / 2;
			this.left.rotation.y = 0;
			this.right.rotation.y = 0;
			this.left.rotation.x = 0;
			this.right.rotation.x = 0;
		}
		if (this.isfalling && this.anims.fall.time > 0.2 && this.anims.fall.time < 0.4)
			this.charge = 0;
		if (this.isfalling && this.anims.fall.time > 0.6)
		{
			this.canmove = 0;
			this.charge = 1;
		}
		if (this.isfalling && !this.anims.fall.enabled)
		{
			this.isfalling = 0;
			this.charge = 0;
			this.anims.fall.stop();
			this.canmove = 1
		}
		this.mixer.update( dt );
		if (this.charge)
		{
			this.charging = THREE.MathUtils.lerp(this.charging, 5, 0.05)
			if (this.anims.load.paused)
			{
				this.anims.fall.play();
				this.anims.load.stop()
				this.isfalling = 1;
			}
		}
		else
			this.charging = THREE.MathUtils.lerp(this.charging, 1, 0.1)
	}
	movelegs()
	{
		let diry = this.controller.yn + this.controller.yp;
		let dirx = this.controller.xn + this.controller.xp;

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
			this.left.rotation.z = THREE.MathUtils.lerp(this.left.rotation.z, this.animleg, 0.1)
			this.right.rotation.z = THREE.MathUtils.lerp(this.right.rotation.z, this.animleg, 0.1)
			this.bone.rotation.y = THREE.MathUtils.lerp(this.bone.rotation.y, this.dir / 8, 0.2);
			if (dirx < 0)
				dirx = 0;
			this.bone.rotation.x = THREE.MathUtils.lerp(this.bone.rotation.x, this.animleg / 10 + -dirx * 2, 0.1);
		}
		else
		{
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
		}
	}
	move () {
		this.movelegs();
		let ym, xm;
		this.bb = new THREE.Box3().setFromObject(this.mesh);
		xm = this.controller.xn + this.controller.xp + this.knockback;
		ym = this.controller.yn + this.controller.yp;

		if (this.charge)
		{
			ym /= 2;
			xm /= 2;
		}
		if (this.mesh.position.y + ym > this.limit.ny && this.mesh.position.y + ym < this.limit.py)
		{
			this.mesh.translateX(ym);
		}
		if (this.mesh.position.x + xm > this.limit.nx && this.mesh.position.x + xm < this.limit.px)
		{
			this.mesh.translateZ(xm);
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
		if (keyCode == this.bind.charge)
		{
			this.controller.charge = 1;
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

		if (keyCode == this.bind.charge)
		{
			this.controller.charge = 0;
		}
	}
	action() {
		if (this.controller.charge == 1 && !this.isfalling)
		{
			this.anims.load.play();
			this.charge = 1;
		}
		if (this.controller.charge == 0 && !this.isfalling && this.charge)
		{
			this.charge = 0;
			this.knockback = this.charging / 10;
			this.anims.load.stop();
		}
	}
	reset() {
		this.anims.fall.stop();
		this.anims.load.stop();
		this.isfalling = 0;
	}
}