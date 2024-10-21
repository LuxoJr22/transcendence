import * as THREE from 'three';
import { SkeletonCollider } from "./skeletoncollider"
import { equal } from "./utils"

export class Bot{
	scene : THREE.Scene
	name : string;
	mesh : THREE.Object3D;
	skeletoncollider : SkeletonCollider;
	left : THREE.Object3D;
	right : THREE.Object3D;
	bone : THREE.Object3D;
	target : THREE.Object3D[];
	dest = [0, 0, 0]
	iscalled = 0
	gravity = -9.81
	movements =  {xp: 0, xn: 0, yp: 0, yn: 0, charge: 0}
	lastmove = 0
	isground = 1
	rotation = 0
	rotationy = 0
	targetx = 0;
	targetz = 0
	dir = 0;
	animleg = 0
	ispicked = 0
	throwed = 0
	moving = 0

	constructor(mesh : THREE.Object3D , scene : THREE.Scene, name : string){
		this.scene = scene
		this.name = name
		this.mesh = mesh.scene
		this.mesh.traverse(function(node : THREE.Object3D) {
            if (node.isMesh)
                node.castShadow = true;
            if (node.isSkinnedMesh)
                node.frustumCulled = false;
        })
		const pick : THREE.Object3D[] = [];
		this.skeletoncollider = new SkeletonCollider(this.mesh, this.scene, pick)
		this.scene.add(this.mesh)
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
		this.target = this.mesh.getObjectByName("Bone001").children;

		this.target = this.target.concat(pick)


	}
	update(dt : number, t : number)
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
			if (!this.ispicked)
			{
				this.mesh.position.y += this.gravity * dt * 3
				this.mesh.rotation.x = THREE.MathUtils.lerp(this.mesh.rotation.x, 0, 0.1)
			}
			this.isground = 0
		}
		else
		{
			if (this.isground == 0)
				this.mesh.rotation.x = 0
			this.isground = 1
			
		}
		if (this.moving && !this.ispicked && !this.iscalled)
		{
			this.movements.xp = 0.1
			this.mesh.translateZ(0.04)
			this.mesh.rotation.y = THREE.MathUtils.lerp(this.mesh.rotation.y, this.rotationy, 0.1)
		}
		else if (!this.iscalled)
			this.movements.xp = 0

		if (this.throwed)
			this.throw()
		if (!this.ispicked)
			this.movelegs()
		else if (this.ispicked)
			this.picked()
		if (this.iscalled)
			this.called()
	}
	called()
	{
		this.mesh.translateZ(0.1)
		this.movements.xp = 0.2
		if (this.mesh.position.x >= this.dest[0] - 0.1 && this.mesh.position.x <= this.dest[0] + 0.1 
			&& this.mesh.position.z >= this.dest[2] - 0.1 && this.mesh.position.z <= this.dest[2] + 0.1)
		{
			this.mesh.position.x = this.dest[0]
			this.mesh.position.z = this.dest[2]
			this.mesh.rotation.y = 0
			this.iscalled = 0
			this.movements.xp = 0
		}
		
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
		if (THREE.MathUtils.randInt(0, 2) == 0 && !this.ispicked && this.isground && !this.throwed && !this.iscalled)
		{
			this.moving = 1
			this.rotationy = THREE.MathUtils.randFloat(0, 3.14)
			this.rotation = THREE.MathUtils.randFloat(-0.01, 0.01)
		}
		if (this.mesh.position.y > 17 || this.mesh.position.y < -17 || this.mesh.position.x > 33 || this.mesh.position.x < -33)
		{
			this.moving = 0;
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