import * as THREE from 'three';
import * as SkeletonUtils from 'three/examples/jsm/utils/SkeletonUtils.js';
import { equal, lerp, random} from "./utils"


export class Bot {
	rightb : THREE.Box3;
	upperb : THREE.Box3;
	leftb : THREE.Box3;
	lowerb : THREE.Box3;
	bb : THREE.Box3;

	left : THREE.Object3D;
	right : THREE.Object3D;
	bone : THREE.Object3D;
	mesh ;
	
	jump = 0;
	jumping = 0;
	moving = 1;
	spectating = 0;
	scoring = 0;
	animleg = Math.PI / 7;
	dir = 0;
	inter = 0;
	place = 0;

	constructor (mesh : THREE.Object3D, collision : THREE.Mesh[]) {
		this.rightb = new THREE.Box3().setFromObject(collision[0]);
		this.upperb = new THREE.Box3().setFromObject(collision[1]);
		this.leftb = new THREE.Box3().setFromObject(collision[2]);
		this.lowerb = new THREE.Box3().setFromObject(collision[3]);
		this.mesh = SkeletonUtils.clone(mesh);
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
		this.bb = new THREE.Box3().setFromObject(this.mesh);
		this.jump = 0;
		this.jumping = 0;
		this.moving = 1;
		this.spectating = 0;
		this.scoring = 0;
		this.animleg = Math.PI / 7;
		this.left.rotation.x = Math.random() * 0.3;
		this.dir = 0;
		this.inter = 0;
		this.place = 0;
		this.mesh.rotation.z = Math.random() * Math.PI * 2;
		if (Math.floor(Math.random() * 2) == 1)
		{
			this.mesh.position.y = random(-17, 17);
			if (Math.floor(Math.random() * 2) == 1)
				this.mesh.position.x = -33;
			else
				this.mesh.position.x = 33;
		}
		else
		{
			this.mesh.position.x = random(-33, 33);
			if (Math.floor(Math.random() * 2) == 1)
				this.mesh.position.y = -17;
			else
				this.mesh.position.y = 17;
		}
	}
	update(){
		if (this.moving)
			this.move();
		else if (this.spectating && this.scoring)
			this.spectate()
		else
			this.anim()
		this.inter = this.bb.intersectsBox(this.leftb) + this.bb.intersectsBox(this.upperb) * -2 + this.bb.intersectsBox(this.rightb) * 3 + this.bb.intersectsBox(this.lowerb) * 4;
		if (this.inter)
		{
			this.moving = 0;
			this.dir = Math.PI / 2 * this.inter;
			if (this.dir == Math.PI * 2)
				this.dir = 0;
		}
	}
	move() {
		var dist = Math.abs(this.left.rotation.x - this.animleg) / 10 + 0.02;
		this.mesh.translateY(dist);
		if (this.mesh.position.y > 17 || this.mesh.position.y < -17 || this.mesh.position.x > 33 || this.mesh.position.x < -33)
		{
			this.mesh.rotation.z = Math.random() * Math.PI * 2;
			if (Math.floor(Math.random() * 2) == 1)
			{
				this.mesh.position.y = random(-17, 17);
				if (Math.floor(Math.random() * 2) == 1)
					this.mesh.position.x = -33;
				else
					this.mesh.position.x = 33;
			}
			else
			{
				this.mesh.position.x = random(-33, 33);
				if (Math.floor(Math.random() * 2) == 1)
					this.mesh.position.y = -17;
				else
					this.mesh.position.y = 17;
			}
		}
		if (this.animleg > 0 && this.left.rotation.x >= this.animleg - 0.01)
			this.animleg *= -1;
		else if (this.animleg < 0 && this.left.rotation.x <= this.animleg + 0.01)
			this.animleg *= -1;
		this.left.rotation.x = THREE.MathUtils.lerp(this.left.rotation.x, this.animleg, 0.1);
		this.right.rotation.x = THREE.MathUtils.lerp(this.right.rotation.x, this.animleg, 0.1);
		this.bb = new THREE.Box3().setFromObject( this.mesh);
	}
	anim()
	{
		this.bone.rotation.x = THREE.MathUtils.lerp(this.bone.rotation.x, Math.PI / 2, 0.1);
		this.left.rotation.x = THREE.MathUtils.lerp(this.left.rotation.x, 0, 0.1);
		this.right.rotation.x = THREE.MathUtils.lerp(this.right.rotation.x, 0, 0.1);
		if (equal(this.bone.rotation.x, Math.PI / 2))
		{
			this.mesh.position.z = THREE.MathUtils.lerp(this.mesh.position.z, -0.2, 0.1);
			this.bone.rotation.y = THREE.MathUtils.lerp(this.bone.rotation.y, Math.PI, 0.03);
			this.mesh.rotation.z = lerp(this.mesh.rotation.z, -this.dir, -0.04);
			if (equal(this.bone.rotation.y, Math.PI) && this.mesh.rotation.z ==  -this.dir)
			{
				this.bone.rotation.y = Math.PI;
				this.spectating = 1;
			}
		}
	}
	spectate()
	{
		if (equal(this.mesh.position.z, -0.2))
		{
			this.jumping = 1;
			this.jump = Math.random() * 0.5;
		}
		else if (equal(this.mesh.position.z, this.jump))
			this.jumping = 0;
		if (this.jumping == 1)
			this.mesh.position.z = THREE.MathUtils.lerp(this.mesh.position.z, this.jump, 0.2);
		else
			this.mesh.position.z = THREE.MathUtils.lerp(this.mesh.position.z,  -0.2, 0.3);
	}
}