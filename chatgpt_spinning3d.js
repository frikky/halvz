
			// Only continue if WebGL is available and working
			//if (gl === null) {
			//	alert(
			//		"Unable to initialize WebGL. Your browser or machine may not support it."
			//	);
			//	return;
			//}

			//// Set clear color to black, fully opaque
			//gl.clearColor(0.0, 0.0, 0.0, 1.0);
			//// Clear the color buffer with specified clear color
			//gl.clear(gl.COLOR_BUFFER_BIT);

		// Set up the canvas element and get the WebGL context
		//var canvas = document.getElementById("canvas");
		//var gl = canvas.getContext("webgl");
		
		// Set up the vertices and indices for a triangle
		var vertices = [  -0.5, -0.5, 0.0,   0.5, -0.5, 0.0,   0.0,  0.5, 0.0];
		var indices = [0, 1, 2];
		
		// Create a buffer to hold the vertices
		var vertexBuffer = gl.createBuffer();
		gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
		gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);
		
		// Create a buffer to hold the indices
		var indexBuffer = gl.createBuffer();
		gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
		gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(indices), gl.STATIC_DRAW);
		
		// Set up the shaders and program
		var vertexShaderSource = `
		  attribute vec3 aVertexPosition;
		  uniform mat4 uModelViewMatrix;
		  void main() {
		    gl_Position = uModelViewMatrix * vec4(aVertexPosition, 1.0);
		  }
		`;
		var fragmentShaderSource = `
		  void main() {
		    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
		  }
		`;
		var vertexShader = gl.createShader(gl.VERTEX_SHADER);
		gl.shaderSource(vertexShader, vertexShaderSource);
		gl.compileShader(vertexShader);
		var fragmentShader = gl.createShader(gl.FRAGMENT_SHADER);
		gl.shaderSource(fragmentShader, fragmentShaderSource);
		gl.compileShader(fragmentShader);
		var program = gl.createProgram();
		gl.attachShader(program, vertexShader);
		gl.attachShader(program, fragmentShader);
		gl.linkProgram(program);
		gl.useProgram(program);
		
		// Set up the attribute and uniform variables
		var aVertexPosition = gl.getAttribLocation(program, "aVertexPosition");
		gl.enableVertexAttribArray(aVertexPosition);
		gl.vertexAttribPointer(aVertexPosition, 3, gl.FLOAT, false, 0, 0);
		var uModelViewMatrix = gl.getUniformLocation(program, "uModelViewMatrix");
		
		// Set up the model-view matrix
		var modelViewMatrix = mat4.create();

  // Animate the triangle by rotating it around the y-axis
  var angle = 0;
  function updateAnimation() {
    angle += 0.01;
    mat4.rotateY(modelViewMatrix, modelViewMatrix, angle);
    
    // Set the model-view matrix as a uniform variable
    gl.uniformMatrix4fv(uModelViewMatrix, false, modelViewMatrix);
    
    // Clear the canvas and draw the triangle
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawElements(gl.TRIANGLES, indices.length, gl.UNSIGNED_SHORT, 0);
    
    // Request the next animation frame
    requestAnimationFrame(updateAnimation);
  }
  
  // Start the animation
  updateAnimation();
