import * as THREE from 'three';
import { SkeletonCollider } from "./skeletoncollider.js"
import { equal } from "./utils.js"

export class Bot{
	constructor(mesh, scene){
		this.scene = scene
		this.mesh = mesh
		this.mesh.traverse(function(node) {
            if (node.isMesh)
                node.castShadow = true;
            if (node.isSkinnedMesh)
                node.frustumCulled = false;
        })
		const pick = []
		this.skeletoncollider = new SkeletonCollider(this.mesh, this.scene, pick)
		this.target = this.mesh.getObjectByName("Bone001").children;
		this.target.concat(this.pick)
		this.scene.add(this.mesh)
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
		this.gravity = -9.81
		this.movements =  {xp: 0, xn: 0, yp: 0, yn: 0, charge: 0}
		this.lastmove = 0
		this.isground = 1
		this.rotation = 0
		this.rotationy = 0
		this.targetx = 0;
		this.targetz = 0
		this.dir = 0;
		this.animleg = 0
		this.ispicked = 0
		this.throwed = 0
		this.moving = 0

	}
	update(dt, t)
	{
		this.skeletoncollider.update()
		if (t > this.lastmove + 6)
		{
			this.move()
			this.lastmove = t
		}
		if (t > this.lastmove + 3)
			this.moving = 0
		if (this.mesh.position.y > 0)
		{
			this.mesh.position.y += this.gravity * dt * 3
			this.mesh.rotation.x = THREE.MathUtils.lerp(this.mesh.rotation.x, 0, 0.1)
			this.isground = 0
		}
		else
			this.isground = 1
		if (this.moving && !this.ispicked)
		{
			this.movements.xp = 0.1
			this.mesh.translateZ(0.06)
			this.mesh.rotation.y = THREE.MathUtils.lerp(this.mesh.rotation.y, this.rotationy, 0.1)
			//this.rotationy += this.rotation
		}
		else
			this.movements.xp = 0

		if (this.throwed)
			this.throw()
		if (!this.ispicked)
			this.movelegs()
		else
			this.picked()
	}
	throw()
	{
		this.mesh.position.x = THREE.MathUtils.lerp(this.mesh.position.x , this.targetx, 0.1);
		this.mesh.position.z = THREE.MathUtils.lerp(this.mesh.position.z, this.targetz, 0.1);
		if (equal(this.mesh.position.x, this.targetx) && equal(this.mesh.position.z, this.targetz))
			this.throwed = 0
	}
	picked()
	{
		let diry = THREE.MathUtils.randFloat(-0.15, 0.15);
		let dirx =  THREE.MathUtils.randFloat(-0.15, 0.15);

		if (dirx != 0)
			this.dir = Math.atan(diry / dirx);
		else
			this.dir = Math.asin(diry * 10 * 2/3);


		if (dirx == 0 && diry == 0)
			this.animleg = 0;
		else if (this.animleg == 0)
			this.animleg = Math.PI / 3;
		if (this.animleg != 0 && Math.abs(this.left.rotation.z) >= Math.abs(this.animleg) - 0.4)
			this.animleg *= -1;
		this.left.rotation.y = -this.dir;
		this.right.rotation.y = -this.dir;
		this.left.rotation.x = 0;
		this.right.rotation.x = 0;
		this.left.rotation.z = THREE.MathUtils.lerp(this.left.rotation.z, this.animleg, 0.1);
		this.right.rotation.z = THREE.MathUtils.lerp(this.right.rotation.z, this.animleg, 0.1);
		this.bone.rotation.y = THREE.MathUtils.lerp(this.bone.rotation.y, this.dir / 8, 0.1);
		if (dirx < 0)
			dirx = 0;
		this.bone.rotation.x = THREE.MathUtils.lerp(this.bone.rotation.x, this.animleg / 20 + -dirx * 0.5, 0.1);
	}
	move()
	{
		if (THREE.MathUtils.randInt(0, 2) == 0 && !this.ispicked && this.isground)
		{
			this.moving = 1
			this.rotationy = THREE.MathUtils.randFloat(0, 3.14)
			this.rotation = THREE.MathUtils.randFloat(-0.01, 0.01)
		}
	}
	movelegs()
	{
		let diry = this.movements.yn + this.movements.yp;
		let dirx = this.movements.xn + this.movements.xp;

		if (dirx != 0)
			this.dir = Math.atan(diry / dirx);
		else
			this.dir = Math.asin(diry * 10 * 2/3);


		if (dirx == 0 && diry == 0)
			this.animleg = 0;
		else if (this.animleg == 0)
			this.animleg = Math.PI / 3;
		if (this.animleg != 0 && Math.abs(this.left.rotation.z) >= Math.abs(this.animleg) - 0.4)
			this.animleg *= -1;
		this.left.rotation.y = -this.dir;
		this.right.rotation.y = -this.dir;
		this.left.rotation.x = 0;
		this.right.rotation.x = 0;
		this.left.rotation.z = THREE.MathUtils.lerp(this.left.rotation.z, this.animleg, 0.025);
		this.right.rotation.z = THREE.MathUtils.lerp(this.right.rotation.z, this.animleg, 0.025);
		this.bone.rotation.y = THREE.MathUtils.lerp(this.bone.rotation.y, this.dir / 8, 0.05);
		if (dirx < 0)
			dirx = 0;
		this.bone.rotation.x = THREE.MathUtils.lerp(this.bone.rotation.x, this.animleg / 20 + -dirx * 0.5, 0.1);
	}
}