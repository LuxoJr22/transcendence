import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
import { equal, lerp } from "./utils.js"

export class Shooter {
	constructor (bind, speed, cam, scene) {
		this.jumpheight = 5;
		this.gravity = -9.81;
		this.target = []
		this.scene = scene;
		this.ySpeed = speed * 2;
		this.camera = cam;
		this.cam = new PointerLockControls(this.camera, document.body);
		this.xSpeed = speed * 2;
		this.bb = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 1), new THREE.MeshStandardMaterial( { color: 0xff0000 }));
		this.scene.add(this.bb);
		this.bbox = new THREE.Box3().setFromObject(this.bb);
		this.raycaster = new THREE.Raycaster();
		this.foot = new THREE.Raycaster();
		this.foot.far = 2
		this.velocity = new THREE.Vector3();
		this.force = new THREE.Vector3();
		this.gamepad = 0;
		this.point = 0;
		this.dir = 0;
		this.grounded = 1;

		this.sphere = new THREE.Mesh(new THREE.SphereGeometry(0.2 , 20, 20), new THREE.MeshBasicMaterial( { color: 0xffc000 } ))
		this.spherebb = new THREE.Sphere(this.sphere.position, 10);
		this.sphere.position.set(0, 0, 0);
		this.scene.add(this.sphere);
		this.animleg = 0
		this.movement = new THREE.Vector3();
		this.movecaster = new THREE.Raycaster();
		this.movecaster.far = 1;

		this.canmove = 1;
		this.isfalling = 0;
		this.direc = new THREE.Vector2()
		this.direction = new THREE.Vector3();
		this.footdir = new THREE.Vector3(0, -1 ,0)
	
		this.bind = bind;

		this.controller = {xp: 0, xn: 0, yp: 0, yn: 0, jump: 0}
	}
	update (dt) {
		this.cam.getDirection(this.direction);
		if ((this.direction.x >= 0.1 || this.direction.x <= -0.1) || (this.direction.z >= 0.1 || this.direction.z <= -0.1))
			this.direc = new THREE.Vector2(this.direction.x, this.direction.z).normalize()
		this.raycaster.set(this.cam.getObject().position, this.direction)
		this.foot.set(this.cam.getObject().position, this.footdir)
		let feet = this.cam.getObject().position.clone();
		this.movecaster.set(feet, this.movement.normalize())
		let d = Math.acos(this.direction.x)
		if (this.direction.z < 0)
			d *= -1;
		if (this.canmove)
			this.move(dt)
		var inter = this.foot.intersectObjects( this.scene.children );
		if (inter[0] && inter[0].distance < 1.4)
			this.cam.getObject().position.y += 0.1;
		
		if (inter[0])
			this.grounded = 1;
		else
			this.grounded = 0;
		this.bb.position.set(this.cam.getObject().position.x, this.cam.getObject().position.y, this.cam.getObject().position.z);
		this.bbox = new THREE.Box3().setFromObject(this.bb);
	}
	move (dt) {
		let ym, xm;
		xm = this.controller.xn + this.controller.xp;
		ym = this.controller.yn + this.controller.yp;
		if (this.controller.jump && this.grounded)
		{
			this.velocity.y = Math.sqrt(this.jumpheight * -2 * this.gravity);
		}
		this.velocity.y += this.gravity * dt;
		if (this.velocity.y < 0 && this.grounded)
			this.velocity.y = 0
		this.cam.getObject().position.y += this.velocity.y * dt;



		let speedif = (100 * ym) - this.velocity.z;
		this.velocity.z += speedif * 0.1;

		let speedifx = (100 * xm) - this.velocity.x;
		this.velocity.x += speedifx * 0.1;

		this.force.x += -this.force.x * 0.05;
		this.force.z += -this.force.z * 0.05;
		this.force.y += -this.force.y * 0.1;
		if (this.force.y < 0 && this.grounded)
			this.force.y = 0
		var test = this.movecaster.intersectObjects( this.scene.children);

		if (this.cam && !test[0])
		{
			this.cam.getObject().position.x += this.velocity.x * dt * this.direc.y * -1;
			this.cam.getObject().position.z += this.velocity.x * dt * this.direc.x;
			this.cam.getObject().position.x += this.velocity.z * dt * this.direc.x;
			this.cam.getObject().position.z += this.velocity.z * dt * this.direc.y;

			this.cam.getObject().position.x += this.force.x * dt;
			this.cam.getObject().position.z += this.force.z * dt;
			this.cam.getObject().position.y += this.force.y * dt;

		}

		this.movement.x = this.velocity.x * dt * this.direc.y * -1 + this.velocity.z * dt * this.direc.x + this.force.x * dt;
		this.movement.y = this.velocity.y * dt + this.force.y * dt;
		this.movement.z = this.velocity.x * dt * this.direc.x + this.velocity.z * dt * this.direc.y + this.force.z * dt;

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