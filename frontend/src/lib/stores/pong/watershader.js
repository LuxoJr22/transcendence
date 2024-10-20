import * as THREE from 'three';

let shade;

(async () => {
    const { generateCausticCanvasTexture } = await import("./waterTexture.js");
    const mapping = generateCausticCanvasTexture(15);

    shade = new THREE.ShaderMaterial({
        uniforms: {
            map: { value: mapping },
            basecolor: { value: new THREE.Color(0x54A0E4) },
            foamcolor: { value: new THREE.Color(0xF5F5F5) },
            time: { value: 1.0 },
            scale: { value: 10.0 },
        },
        fragmentShader: `
        varying vec2 vUv;
        uniform sampler2D map;
        uniform vec3 basecolor;
        uniform vec3 foamcolor;
        uniform float time;
        uniform float scale;
        void main() {
            gl_FragColor.a = 1.0;
            vec3 color = texture2D( map, vUv * scale +
                0.5*vec2( cos(time*0.001*0.1), sin(time*0.001*0.1)) +
                0.1*vec2( cos(time*0.0012+3.2*scale*vUv.x), sin(time*0.001+3.0*scale*vUv.y))).rgb;
            vec3 color2 = texture2D( map, vUv * scale * 1.3+
                0.8*vec2(cos(time*0.001*0.1), sin(time*0.001*0.1)) +
                0.01*vec2(cos(1.7 + time*0.0012+3.2*scale*vUv.x), sin(1.7 + time*0.001+3.0*scale*vUv.y))).rgb;
            float d = 0.0;
            gl_FragColor.rgb = mix(basecolor * clamp(1.0 - color2, 0.9, 1.0), foamcolor, color);
        }`,
        vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);    
        }
        `
    });
})();

export { shade };