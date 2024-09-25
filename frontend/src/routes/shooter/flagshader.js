import * as THREE from 'three';

export const flagshader = new THREE.ShaderMaterial( {
	transparent : true,
	uniforms: {
	time: { value : 0},
	},
	fragmentShader: `
	uniform float time;
	void main() {
		if (tan(time) > 0.0)
			gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0 - tan(time));
		else
			gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);

			
	}`,
	vertexShader: `
	uniform float time;
	void main() {
		vec4 result;

		result = vec4(position.x , position.y , position.z - tan(time), 1.0);
		result.x += result.x * cos(time * 2.0) / 2.0;

		result.y += result.y * cos(time * 2.0) / 2.0;

		gl_Position = projectionMatrix * modelViewMatrix * result;
	}
	`
});