console.log("three.js script loaded");

let scene, camera, renderer, model;
let clock = new THREE.Clock();

init();
animate();

// scene & camera
function init(){
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    // renderer
    renderer = new THREE.WebGLRenderer({
        canvas: document.getElementById("sneaker-bg"),
        antialias: true,
        alpha: true
     });
    renderer.setSize(window.innerWidth, window.innerHeight);

    // lighting
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(5, 5, 5);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0xffffff, 0.6));

    // load odel
    const loader = new THREE.GLTFLoader();
    loader.load(
        modelPath,
        function (gltf) {
            console.log("Model loaded successfully");
            model = gltf.scene;
            model.scale.set(1.5, 1.5, 1.5);
            scene.add(model);
        },
        function (xhr) {
            console.log(`Model loading: ${(xhr.loaded / xhr.total) * 100}% loaded`);
        }, 
        function (error) {
            console.error("Error loading model:", error);   
        }
    );
    // Resize listener
    window.addEventListener('resize', onWindowResize, false);
}

function onWindowResize(){
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix(); //Chat it
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);

    if (model) {
        // Rotate & Float
        model.rotation.y = Math.PI / 4; //+= 0.0005;
        let t = clock.getElapsedTime();
        model.position.y = Math.sin(t) * 0.2; //float motion
    }
    renderer.render(scene, camera);
}
