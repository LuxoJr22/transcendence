import * as THREE from 'three';

export class Bot{
	constructor(mesh, scene){
		this.scene = scene
		this.mesh = mesh
		this.left = this.mesh.getObjectByName("Bone003L");
		this.right = this.mesh.getObjectByName("Bone003R");
		this.bone = this.mesh.getObjectByName("Bone");
		this.gravity = -9.81
		this.movements =  {xp: 0, xn: 0, yp: 0, yn: 0, charge: 0}
		this.isground = 1
		this.rotation = 0
		this.rotationy = 0
		this.dir = 0;
		this.animleg = 0
		this.ispicked = 0
		this.moving = 0
		this.foot = new THREE.Raycaster();
		this.foot.far = 0.5
		this.footdir = new THREE.Vector3(0, -1 ,0)

	}
	update(dt)
	{
		this.foot.set(new THREE.Vector3(this.mesh.position.x, this.mesh.position.y + 0.5, this.mesh.position.z), this.footdir)
		var inter = this.foot.intersectObjects( this.scene.children);
		if ((!(inter.length > 0) || (inter.length == 1 && inter[0].object.name == "frontplane")) && !this.ispicked)
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
		if (!this.ispicked)
			this.movelegs()
		else
			this.picked()
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