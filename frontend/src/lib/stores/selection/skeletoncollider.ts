import * as THREE from "three"

export class SkeletonCollider {
	distance = 0
	v1 = new THREE.Vector3()
	v2 = new THREE.Vector3()
	bones : THREE.Object3D[] = []
	material = new THREE.MeshBasicMaterial({
		color: 0xff0000,
		wireframe: true,
		depthTest: false,
	})
	constructor(object : THREE.Object3D, scene : THREE.Scene, pickables: THREE.Object3D[]) {
		object.traverse((child : THREE.Object3D) => {
			if (child.isBone) {
				if (child.parent && child.parent.type === 'Bone') {
					this.bones.push(child)
					child.getWorldPosition(this.v1)
					child.parent.getWorldPosition(this.v2)
					this.distance = this.v2.distanceTo(this.v1)
					let g
					switch (child.name) {
						case 'Bone001':
						{
							g = new THREE.BoxGeometry(3, 1, 1)
							g.translate(0, this.distance / 2 - 0.3, 0)
							break;
						}
						default:
						{
							g = new THREE.BoxGeometry(0.2, this.distance, 0.2)
							g.translate(0, this.distance / 2, 0)
							break
						}
					}
					
					const m = new THREE.Mesh(g, this.material)
					m.visible = false
					scene.add(m)

					child.userData.m = m
					pickables.push(m)
				}
			}
		})
	}

	update() {
		this.bones.forEach((b) => {
			b.getWorldPosition(b.userData.m.position)
			b.getWorldQuaternion(b.userData.m.quaternion)
		})
	}
}