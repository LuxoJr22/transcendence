import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
import { equal, lerp } from "./utils.js"

export class Shooter {
	constructor (mesh, bind, speed, cam, scene) {
		this.scene = scene;
		this.ySpeed = speed * 2;
		this.camera = cam;
		this.cam = new PointerLockControls(this.camera, document.body);;
		this.xSpeed = speed * 2;
		this.mesh = mesh.scene;
		this.bb = new THREE.Box3().setFromObject( mesh.scene);
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
		this.raycaster = new THREE.Raycaster();
		this.gamepad = 0;
		this.point = 0;
		this.dir = 0;
		this.canJump = 1;
		this.jumping = 0;

		this.sphere = new THREE.Mesh(new THREE.SphereGeometry(0.2 , 20, 20), new THREE.MeshBasicMaterial( { color: 0xffc000 } ))
		this.sphere.position.set(0, 0, 0);
		this.scene.add(this.sphere);
		this.animleg = 0

		this.canmove = 1;
		this.isfalling = 0;
		this.knockback = 0;
		this.direction = new THREE.Vector3();
	
		this.bind = bind;

		this.controller = {xp: 0, xn: 0, yp: 0, yn: 0, jump: 0}
	}
	update (dt) {
		this.cam.getDirection(this.direction);
		this.raycaster.set(this.cam.getObject().position, this.direction)
		let d = Math.acos(this.direction.x)
		if (this.direction.z < 0)
			d *= -1;
		this.mesh.rotation.y = -d + Math.PI / 2;
		this.knockback = THREE.MathUtils.lerp(this.knockback, 0, 0.1)
		this.action();
	}
	mousedown()
	{
		var intersects = this.raycaster.intersectObjects( this.scene.children );

		if (intersects[0] && intersects[ 0 ].object != this.sphere)
		{
			this.sphere.position.set(intersects[0].point.x, intersects[0].point.y ,intersects[0].point.z );

		}
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
		if (this.controller.jump && this.jumping)
			this.cam.getObject().position.y = THREE.MathUtils.lerp(this.cam.getObject().position.y, 3, 0.1);
		else
			this.cam.getObject().position.y = lerp(this.cam.getObject().position.y, 0.5, -0.1);
		if (this.cam.getObject().position.y + 0.1 > 3)
			this.jumping = 0;
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
			if (equal(this.cam.getObject().position.y, 0.5))
				this.jumping = 1;
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