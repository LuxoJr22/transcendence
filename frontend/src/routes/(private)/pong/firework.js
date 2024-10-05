import * as THREE from 'three';



export class Firework{
	constructor(scene, spawn ) {
        this.spawn = spawn
        this.scene    = scene; 
        this.done     = false; 
        this.speed = 0.5;
        this.dest     = []; 
        this.colors   = []; 
        this.geometry = null;
        this.points   = null;
        this.material = new THREE.PointsMaterial({
            size: 0.2,
            color: 0xffffff,
            opacity: 1,
            vertexColors: true,
            transparent: true,
            //depthTest: false,
        });
        this.launch(); 
    }
	explode( vector ) {
        this.scene.remove( this.points );  
        this.dest     = []; 
        this.colors   = []; 
        let points = []
        
        for( var i = 0; i < 80; i++ )
        {
            var color = new THREE.Color();
            color.setHSL( THREE.MathUtils.randFloat( 0, 1 ), 1, 0.5 );
            this.colors = this.colors.concat( color.toArray()); 

            var from = new THREE.Vector3( 
                THREE.MathUtils.randInt( vector.x, vector.x), 
                THREE.MathUtils.randInt( vector.y, vector.y ), 
                THREE.MathUtils.randInt( vector.z, vector.z )
            ); 
            var to = new THREE.Vector3(
                THREE.MathUtils.randInt( vector.x - 10, vector.x + 10 ), 
                THREE.MathUtils.randInt( vector.y - 10, vector.y + 10 ), 
                THREE.MathUtils.randInt( vector.z - 10, vector.z + 10 )
            ); 
            points.push( from ); 
            this.dest.push( to ); 
        }
        this.geometry = new THREE.BufferGeometry().setFromPoints(points);
        this.geometry.setAttribute( 'color', new THREE.BufferAttribute( new Float32Array(this.colors), 3 ) );
        this.points   = new THREE.Points( this.geometry, this.material);
        this.scene.add( this.points );  
    }
    reset() {
        this.scene.remove( this.points );  
        this.dest     = []; 
        this.colors   = []; 
        this.geometry = null;
        this.points   = null;
    }
	update(dt) {
        if( this.points && this.geometry )
        {

            let vertices = this.geometry.attributes.position.array;
            for(let i = 0; i < this.geometry.attributes.position.count; i++){
                vertices[ i * 3 + 0 ] += ( this.dest[i].x - vertices[ i * 3 + 0 ] ) / this.speed * dt;
                vertices[ i * 3 + 1 ] += ( this.dest[i].y - vertices[ i * 3 + 1 ] ) / this.speed * dt;
                vertices[ i * 3 + 2 ] += ( this.dest[i].z - vertices[ i * 3 + 2 ] ) / this.speed * dt;
                if ( this.geometry.attributes.position.count == 1) 
                {
                    if( Math.ceil( vertices[2] ) > ( this.dest[0].z - this.speed ) )
                    {
                        this.explode( new THREE.Vector3(vertices[0], vertices[1], vertices[2])); 
                        return; 
                    }
                }
                if( i > 1 ) 
                {
                    this.material.opacity -= 0.005 * dt; 
                }
                if( this.material.opacity <= 0 )
                {
                    this.reset(); 
                    this.done = true; 
                    return; 
                }
            }
            this.geometry.attributes.position.needsUpdate = true;
        }
    }
    launch() {
        var x = THREE.MathUtils.randInt( this.spawn[0], this.spawn[0] * 1.5); 
        var y = THREE.MathUtils.randInt( -10, 10);
        var z = THREE.MathUtils.randInt( 7,  13); 
        
        var from = new THREE.Vector3( x, y, -10 ); 
        var to   = new THREE.Vector3( x, y, z ); 
        
        var color = new THREE.Color();
        color.setHSL( THREE.MathUtils.randFloat( 0.1, 0.9 ), 1, 0.9 );
        this.colors = this.colors.concat( color.toArray()); 

        let points = []
        points.push( from ); 
        
        this.geometry = new THREE.BufferGeometry().setFromPoints(points);
        this.geometry.setAttribute( 'color', new THREE.BufferAttribute( new Float32Array(this.colors), 3 ) );
        this.points   = new THREE.Points( this.geometry, this.material );
        
        
        
        this.dest.push( to ); 
        //this.colors.concat( color ); 
        this.scene.add( this.points );  
    }
};
    












