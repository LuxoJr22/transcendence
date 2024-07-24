import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
import { equal, lerp } from "./utils.js"

export class Shooter {
	constructor (mesh, bind, speed, cam, scene, target, collider, pickable) {
		this.jumpheight = 5;
		this.gravity = -9.81;
		this.collider = collider;
		this.target = target.getObjectByName("Bone001").children;
		this.target = this.target.concat(pickable)
		this.scene = scene;
		this.ySpeed = speed * 2;
		this.camera = cam;
		this.cam = new PointerLockControls(this.camera, document.body);
		this.lastpos = this.cam.getObject().position.clone();
		this.xSpeed = speed * 2;
		this.mesh = mesh.scene;
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
		this.bb = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 1), new THREE.MeshStandardMaterial( { color: 0xff0000 }));
		this.scene.add(this.bb);
		this.bbox = new THREE.Box3().setFromObject(this.bb);
		this.raycaster = new THREE.Raycaster();
		this.foot = new THREE.Raycaster();
		this.foot.far = 1.6
		this.velocity = new THREE.Vector3();
		this.gamepad = 0;
		this.point = 0;
		this.dir = 0;
		this.grounded = 1;

		this.sphere = new THREE.Mesh(new THREE.SphereGeometry(0.2 , 20, 20), new THREE.MeshBasicMaterial( { color: 0xffc000 } ))
		this.spherebb = new THREE.Sphere(this.sphere.position, 10);
		this.sphere.position.set(0, 0, 0);
		this.scene.add(this.sphere);
		this.animleg = 0

		this.canmove = 1;
		this.isfalling = 0;
		this.direction = new THREE.Vector3();
		this.footdir = new THREE.Vector3(0, -1 ,0)
	
		this.bind = bind;

		this.controller = {xp: 0, xn: 0, yp: 0, yn: 0, jump: 0}
	}
	update (dt) {
		this.cam.getDirection(this.direction);
		this.raycaster.set(this.cam.getObject().position, this.direction)
		this.foot.set(this.cam.getObject().position, this.footdir)
		let d = Math.acos(this.direction.x)
		if (this.direction.z < 0)
			d *= -1;
		this.mesh.rotation.y = -d + Math.PI / 2;
		if (this.canmove)
			this.move(dt)
		var inter = this.foot.intersectObjects( this.scene.children );

		if (inter[0])
			this.grounded = 1;
		else
			this.grounded = 0;
		this.bb.position.set(this.cam.getObject().position.x, this.cam.getObject().position.y, this.cam.getObject().position.z);
		this.bbox = new THREE.Box3().setFromObject(this.bb);
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
	move (dt) {
		this.movelegs();
		if (!this.bbox.intersectsBox(this.collider[0]) && !this.bbox.intersectsBox(this.collider[1]))
			this.lastpos = this.cam.getObject().position.clone();
		let ym, xm;
		xm = this.controller.xn + this.controller.xp;
		ym = this.controller.yn + this.controller.yp;
		if (this.controller.jump && this.grounded)
		{
			this.velocity.y = Math.sqrt(this.jumpheight * -2 * this.gravity);
		}
		this.velocity.y += this.gravity * dt;
		if (this.velocity.y < 0 && this.grounded)
		{
			this.velocity.y = 0
		}
		this.cam.getObject().position.y += this.velocity.y * dt;



		let speedif = (100 * ym) - this.velocity.z;
		this.velocity.z += speedif * 0.1;

		let speedifx = (100 * xm) - this.velocity.x;
		this.velocity.x += speedifx * 0.1;

		if (this.cam && !this.bbox.intersectsBox(this.collider[0]) && !this.bbox.intersectsBox(this.collider[1]))
		{
			//console.log((this.velocity.x * dt * this.direction.z * -1) + (this.velocity.z * dt * this.direction.x))
			this.cam.getObject().position.x += this.velocity.x * dt * this.direction.z * -1;
			this.cam.getObject().position.z += this.velocity.x * dt * this.direction.x;
			this.cam.getObject().position.x += this.velocity.z * dt * this.direction.x;
			this.cam.getObject().position.z += this.velocity.z * dt * this.direction.z;
		}




		if (this.bbox.intersectsBox(this.collider[0]) || this.bbox.intersectsBox(this.collider[1]))
			this.cam.getObject().position.set(this.lastpos.x, this.cam.getObject().position.y, this.lastpos.z);

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
}