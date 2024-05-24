import * as THREE from 'three';
import { Vector3 } from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 0.1, 1000 );
scene.background = new THREE.Color(0x999999);

const loader = new GLTFLoader()


var bar;
var mixer;
var charge = 0;


const gltf = await loader.loadAsync('bar.glb');
bar = gltf.scene;
gltf.scene.position.set(-10, 0, -1.5);
gltf.scene.scale.set(0.5, 0.5, 0.5);
gltf.scene.rotation.y = Math.PI / 2;
gltf.scene.rotation.x = Math.PI / 2;
mixer = new THREE.AnimationMixer( gltf.scene );
var bb = new THREE.Box3().setFromObject(gltf.scene);

let anim = mixer.clipAction( gltf.animations[ 3 ] );
let load = mixer.clipAction( gltf.animations[ 1 ] );
let fall = mixer.clipAction( gltf.animations[ 2 ] );
load.setLoop(THREE.LoopOnce);
load.clampWhenFinished = true;
fall.setLoop(THREE.LoopOnce);
anim.play();
scene.add(bar);




const geometry2 = new THREE.BoxGeometry( 1, 3, 1 ); 
const material2 = new THREE.MeshPhongMaterial( {color: 0x00ffff} ); 
const rect2 = new THREE.Mesh( geometry2, material2 ); 
scene.add( rect2 );

let bbrect2 = new THREE.Box3(new Vector3(), new Vector3());
bbrect2.setFromObject(rect2);

rect2.position.set(10, 0, 0);




const geo = new THREE.SphereGeometry( 0.8, 32, 16); 
const mat = new THREE.MeshPhongMaterial( { color: 0xffff00 } ); 
const sphere = new THREE.Mesh( geo, mat );
scene.add( sphere );

let spherebb = new THREE.Sphere(sphere.position, 1);



const texture = new THREE.TextureLoader().load( "field.png" );

texture.wrapS = THREE.RepeatWrapping;

texture.wrapT = THREE.RepeatWrapping;

let m = new THREE.MeshLambertMaterial({ map : texture });


const plane1 = new THREE.Mesh(new THREE.PlaneGeometry(38, 18), m);
plane1.overdraw = true;
plane1.position.set(0, 0, -4);
plane1.receiveShadow = true;

scene.add(plane1);


const light = new THREE.AmbientLight(0xffffff)
scene.add(light)

const dl = new THREE.DirectionalLight( 0xffffff, 3 );
dl.position.set( 0, 0, 5 );
scene.add( dl );



const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );


camera.position.z = 20;

var xSpeed = 0.1;
var ySpeed = 0.1;

var xmv = 0;
var xmvp = 0;
var ymv = 0;
var ymvp = 0;

var xmv2 = 0;
var ymv2 = 0;
var ballspeed = 0.2;
var charging = 1;
var isfalling = 0;
var canmove = 1;


document.addEventListener("keydown", onDocumentKeyDown, false);
document.addEventListener("keyup", onDocumentKeyUp, false);

function onDocumentKeyDown(event) {
    var keyCode = event.which;
    if (isfalling)
        return;
    if (keyCode == 90)
        ymvp = ySpeed;
    if (keyCode == 83)
        ymv = -ySpeed;
    if (keyCode == 81)
        xmv = -xSpeed;
    if (keyCode == 68)
        xmvp = xSpeed;

    if (keyCode == 32)
    {
        anim.stop();
        load.play();
        charge = 1;
    }
    if (keyCode == 38)
        ymv2 = ySpeed;
    if (keyCode == 40)
        ymv2 = -ySpeed;
    if (keyCode == 37)
        xmv2 = -xSpeed;
    if (keyCode == 39)
        xmv2 = xSpeed;
};

function onDocumentKeyUp(event) {
    var keyCode = event.which;
    if (isfalling)
        return;
    if (keyCode == 90)
        ymvp = 0;
    if (keyCode == 83)
        ymv = 0;
    if (keyCode == 81)
        xmv = 0;
    if (keyCode == 68)
        xmvp = 0;

    if (keyCode == 32)
    {
        charge = 0;
        load.stop();
        anim.play();
    }

    if (keyCode == 38)
        ymv2 = 0;
    if (keyCode == 40)
        ymv2 = 0;
    if (keyCode == 37)
        xmv2 = 0;
    if (keyCode == 39)
        xmv2 = 0;
};

const controls = new OrbitControls( camera, renderer.domElement );
				controls.target.set( 0, 1, 0 );
				controls.update();

let t = 0;
const clock = new THREE.Clock();

let balldir = -0.1;
let balldiry = 0

function moveBall()
{
    sphere.translateX(balldir);
    sphere.translateY(balldiry);
    if (sphere.position.x >= 15 || sphere.position.x <= -15)
    {
        sphere.position.set(0, 0, 0);
        rect2.position.set(10, 0, 0);
        bar.position.set(-10, 0, -1.5);
        balldiry = 0
    }
    if (sphere.position.y >= 7 || sphere.position.y <= -7 )
        balldiry *= -1;

}

function checkCollision() {
    if (bbrect2.intersectsSphere(spherebb))
    {
        balldir = -0.5;
        balldiry = (sphere.position.y - rect2.position.y) * 0.1;
    }
    if (bb.intersectsSphere(spherebb) && charge == 0)
    {
        balldir = 0.5 * charging;
        balldiry = (sphere.position.y - bar.position.y) * 0.1;
    }
    if (balldir < 0)
    {
        balldir = THREE.MathUtils.lerp(balldir, -ballspeed, 0.05);
    }
    if (balldir > 0)
    {
        balldir = THREE.MathUtils.lerp(balldir, ballspeed, 0.05);
    }
}



function animate() {
	requestAnimationFrame( animate );
    const dt = clock.getDelta();
    t += dt;

    if (isfalling && fall.time > 0.2 && fall.time < 0.4)
        charge = 0;
    if (isfalling && fall.time > 0.6)
    {
        canmove = 0;
        charge = 1;
    }
    if (isfalling && !fall.enabled)
    {
        isfalling = 0;
        charge = 0;
        fall.stop();
        anim.play();
        canmove = 1
    }
    if (ymvp + ymv != 0 || xmv + xmvp || charge || isfalling)
        mixer.update( dt );
    if (charge)
    {
        charging = THREE.MathUtils.lerp(charging, 5, 0.05)
        if (load.paused)
        {
            fall.play();
            load.stop()
            isfalling = 1;
        }
    }
    else
        charging = THREE.MathUtils.lerp(charging, 1, 0.1)
    bb = new THREE.Box3().setFromObject(gltf.scene);
    bbrect2.copy( rect2.geometry.boundingBox).applyMatrix4(rect2.matrixWorld);
    if (canmove)
    {
        bar.translateZ(xmv + xmvp);
        bar.translateX(ymv + ymvp);
    }
    rect2.translateY(ymv2);
    rect2.translateX(xmv2);
    //moveBall();
    checkCollision();
	renderer.render( scene, camera );
}

animate();