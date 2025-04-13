// Replace your existing upload functionality with this:

document.addEventListener('DOMContentLoaded', function() {
  const dropArea = document.getElementById('drop-area');
  const fileInput = document.getElementById('fileInput');
  const uploadButton = document.getElementById('uploadButton');
  let selectedFile = null;

  // Highlight drop area when item is dragged over it
  ['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
  });

  // Prevent default drag behaviors
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
  });

  // Handle dropped files
  dropArea.addEventListener('drop', handleDrop, false);

  // Handle file selection via browse button
  fileInput.addEventListener('change', function() {
    if (this.files.length) {
      handleFiles(this.files);
    }
  });

  // Upload button click handler
  uploadButton.addEventListener('click', uploadFile);

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight() {
    dropArea.classList.add('highlight');
  }

  function unhighlight() {
    dropArea.classList.remove('highlight');
  }

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
  }

  function handleFiles(files) {
    if (files.length) {
      selectedFile = files[0];
      
      // Create preview
      const preview = document.createElement('div');
      preview.className = 'image-preview';
      
      if (selectedFile.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
          preview.style.backgroundImage = `url(${e.target.result})`;
          preview.style.backgroundSize = 'cover';
          preview.style.backgroundPosition = 'center';
        };
        reader.readAsDataURL(selectedFile);
      } else {
        preview.textContent = selectedFile.name;
      }
      
      // Clear drop area and add preview
      dropArea.querySelectorAll('.image-preview').forEach(el => el.remove());
      dropArea.appendChild(preview);
    }
  }

  async function uploadFile() {
    if (!selectedFile) {
      alert('Please select an image first');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // Show loading state
      uploadButton.disabled = true;
      uploadButton.innerHTML = '<span>ANALYZING...</span><div class="btn-pulse"></div>';

      const response = await fetch('/upload', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Upload failed');
      }

      // Handle successful upload and prediction
      displayResults(data);
      
    } catch (error) {
      console.error('Upload error:', error);
      alert(`Upload failed: ${error.message}`);
    } finally {
      // Reset button state
      uploadButton.disabled = false;
      uploadButton.innerHTML = '<span>INITIATE SCAN</span><div class="btn-pulse"></div>';
    }
  }

  function displayResults(data) {
    // Navigate to results page (if using SPA approach)
    document.querySelector('[data-route="results"]').style.display = 'block';
    document.querySelector('[data-route="home"]').style.display = 'none';
    
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(navLink => {
      navLink.classList.remove('active');
    });
    document.querySelector('[data-route="results"]').classList.add('active');
    
    // Display the uploaded image
    const resultImage = document.querySelector('.result-image .image-placeholder');
    resultImage.style.backgroundImage = `url(${data.filename})`;
    resultImage.style.backgroundSize = 'cover';
    resultImage.style.backgroundPosition = 'center';
    
    // Display diagnosis
    const diagnosisElement = document.querySelector('.diagnosis-result');
    diagnosisElement.innerHTML = `
      <span class="severity ${getSeverityClass(data.prediction.class)}">
        ${data.prediction.class.toUpperCase()}
      </span>
      <div class="confidence">
        <div class="confidence-bar" style="width: ${data.prediction.confidence * 100}%"></div>
        <span>${Math.round(data.prediction.confidence * 100)}% CONFIDENCE</span>
      </div>
    `;
  }

  function getSeverityClass(className) {
    // Customize based on your class names
    if (className.toLowerCase().includes('high') || className.toLowerCase().includes('malignant')) {
      return 'high';
    } else if (className.toLowerCase().includes('moderate')) {
      return 'moderate';
    } else {
      return 'low';
    }
  }
});

document.querySelector('.upload-btn').addEventListener('click', async function() {
  const fileInput = document.getElementById('fileInput');
  if (fileInput.files.length === 0) {
      alert('Please select an image first');
      return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  try {
      this.disabled = true;
      this.innerHTML = '<span>ANALYZING...</span>';

      const response = await fetch('/upload', {
          method: 'POST',
          body: formData
      });

      const data = await response.json();

      if (response.ok) {
          // Display results
          displayResults(data);
      } else {
          alert(data.error || 'Error uploading file');
          this.disabled = false;
          this.innerHTML = '<span>INITIATE SCAN</span>';
      }
  } catch (error) {
      console.error('Error:', error);
      alert('An error occurred during upload');
      this.disabled = false;
      this.innerHTML = '<span>INITIATE SCAN</span>';
  }
});

function displayResults(data) {
  // Navigate to results page (if using SPA approach)
  document.querySelector('[data-route="results"]').style.display = 'block';
  document.querySelector('[data-route="home"]').style.display = 'none';
  
  // Update active nav link
  document.querySelectorAll('.nav-link').forEach(navLink => navLink.classList.remove('active'));
  document.querySelector('[data-route="results"]').classList.add('active');
  
  // Display the uploaded image
  const resultImage = document.querySelector('.result-image .image-placeholder');
  resultImage.style.backgroundImage = `url(/static/${data.filename})`;
  resultImage.style.backgroundSize = 'cover';
  resultImage.style.backgroundPosition = 'center';
  
  // Display diagnosis
  const diagnosisElement = document.querySelector('.diagnosis-result');
  diagnosisElement.innerHTML = `
      <span class="severity ${getSeverityClass(data.prediction.class)}">${data.prediction.class.toUpperCase()}</span>
      <div class="confidence">
          <div class="confidence-bar" style="width: ${data.prediction.confidence * 100}%"></div>
          <span>${Math.round(data.prediction.confidence * 100)}% CONFIDENCE</span>
      </div>
  `;
  
  // You can add more result display logic here
}

function getSeverityClass(className) {
  // Customize this based on your class names
  if (className.toLowerCase().includes('high') || className.toLowerCase().includes('malignant')) {
      return 'high';
  } else if (className.toLowerCase().includes('moderate')) {
      return 'moderate';
  } else {
      return 'low';
  }
}
// File Upload Handling
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.querySelector('.upload-btn');
const uploadBox = document.querySelector('.upload-box');
const imagePreview = document.createElement('div');
imagePreview.className = 'image-preview';
uploadBox.appendChild(imagePreview);

// Add event listeners
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, preventDefaults, false);
});

['dragenter', 'dragover'].forEach(eventName => {
  dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, unhighlight, false);
});

dropArea.addEventListener('drop', handleDrop, false);
fileInput.addEventListener('change', handleFiles);
uploadBtn.addEventListener('click', handleUpload);

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

function highlight() {
  uploadBox.classList.add('highlight');
}

function unhighlight() {
  uploadBox.classList.remove('highlight');
}

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt.files;
  handleFiles({ target: { files } });
}

function handleFiles(e) {
  const files = e.target.files;
  if (files.length) {
    const file = files[0];
    if (file.type.match('image.*')) {
      const reader = new FileReader();
      reader.onload = function(event) {
        imagePreview.style.backgroundImage = `url(${event.target.result})`;
        uploadBox.classList.add('has-image');
      };
      reader.readAsDataURL(file);
    } else {
      showError('Please upload an image file (JPEG, PNG)');
    }
  }
}

function handleUpload() {
  if (!fileInput.files.length) return;
  
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);
  
  // Show loading state
  uploadBtn.classList.add('uploading');
  uploadBtn.disabled = true;
  
  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Upload failed');
    }
    return response.json();
  })
  .then(data => {
    // Handle successful upload
    displayResults(data);
  })
  .catch(error => {
    showError(error.message);
  })
  .finally(() => {
    uploadBtn.classList.remove('uploading');
    uploadBtn.disabled = false;
  });
}

function showError(message) {
  const errorElement = document.createElement('div');
  errorElement.className = 'upload-error';
  errorElement.textContent = message;
  
  // Remove existing error if any
  const existingError = uploadBox.querySelector('.upload-error');
  if (existingError) {
    existingError.remove();
  }
  
  uploadBox.appendChild(errorElement);
  setTimeout(() => {
    errorElement.style.opacity = '1';
  }, 10);
}

function displayResults(data) {
  // Your existing results display logic
  console.log('Upload successful:', data);
  // Navigate to results page or update UI
}