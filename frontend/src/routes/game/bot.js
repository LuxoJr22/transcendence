import * as THREE from 'three';
import * as SkeletonUtils from 'three/examples/jsm/utils/SkeletonUtils.js';

export class Bot {
	constructor (mesh, start, collision) {
		this.rightb = new THREE.Box3().setFromObject(collision[0]);
		this.upperb = new THREE.Box3().setFromObject(collision[1]);
		this.leftb = new THREE.Box3().setFromObject(collision[2]);
		this.lowerb = new THREE.Box3().setFromObject(collision[3]);
		this.mesh = SkeletonUtils.clone(mesh);
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
		this.bb = new THREE.Box3().setFromObject(this.mesh);
		this.moving = 1;
		this.spectating = 0;
		this.animleg = Math.PI / 7;
		this.left.rotation.x = start;
		this.dir = Math.PI * 3/ 2;
		this.bone.rotation.z = -this.dir;
	}
	random(min, max)
	{
		return (Math.random() * (max - min)) + min;
	}
	update(){
		var inter;
		if (this.moving)
			this.move();
		else if (this.spectating)
			this.spectate()
		else
			this.anim()
		inter = this.bb.intersectsBox(this.rightb) + this.bb.intersectsBox(this.lowerb) * 2 + this.bb.intersectsBox(this.leftb) * 3 + this.bb.intersectsBox(this.upperb) * 4;
		if (inter)
		{
			this.moving = 0;
			this.dir = Math.PI / 2 * inter;
			if (this.dir == Math.PI * 2)
				this.dir = 0;
		}
	}
	move() {
		var dist = Math.abs(this.left.rotation.x - this.animleg) / 10 + 0.02;
		this.mesh.translateY(dist * Math.cos(this.dir));
		this.mesh.translateX(dist * Math.sin(this.dir));
		if (this.mesh.position.y > 17 || this.mesh.position.y < -17 || this.mesh.position.x > 33 || this.mesh.position.x < -33)
		{
			this.dir = Math.random() * Math.PI * 2;
			this.bone.rotation.z = -this.dir;
		}
		if (this.mesh.position.y > 17 || this.mesh.position.y < -17 || this.mesh.position.x > 33 || this.mesh.position.x < -33)
		{
			if (Math.floor(Math.random() * 2) == 1)
			{
				this.mesh.position.y = this.random(-17, 17);
				if (Math.floor(Math.random() * 2) == 1)
					this.mesh.position.x = -33;
				else
					this.mesh.position.x = 33;
			}
			else
			{
				this.mesh.position.x = this.random(-33, 33);
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
		this.bone.rotation.z = THREE.MathUtils.lerp(this.bone.rotation.z, -this.dir, 0.1);
		this.left.rotation.x = THREE.MathUtils.lerp(this.left.rotation.x, 0, 0.1);
		this.right.rotation.x = THREE.MathUtils.lerp(this.right.rotation.x, 0, 0.1);
		if (this.bone.rotation.z >= -this.dir - 0.01 && this.bone.rotation.z <= -this.dir + 0.01)
		{
			this.mesh.position.z = THREE.MathUtils.lerp(this.mesh.position.z, 0, 0.1);
			if (this.dir == 0 || this.dir == Math.PI)
				this.mesh.rotation.x = THREE.MathUtils.lerp(this.mesh.rotation.x, this.dir + Math.PI / 2, 0.1);	
			else 
				this.mesh.rotation.y = THREE.MathUtils.lerp(this.mesh.rotation.y, this.dir - Math.PI, 0.1);
		}
	}
	spectate()
	{

	}
}