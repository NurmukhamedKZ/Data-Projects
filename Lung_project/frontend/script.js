 // Configuration
const CONFIG = {
    API_URL: 'https://tb-classifier-backend.onrender.com',  // Update with your FastAPI server URL
    MAX_FILE_SIZE: 10 * 1024 * 1024,   // 10MB
    ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/jpg']
};

// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const previewSection = document.getElementById('previewSection');
const previewImage = document.getElementById('previewImage');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const removeBtn = document.getElementById('removeBtn');
const closeErrorBtn = document.getElementById('closeErrorBtn');
const spinner = document.getElementById('spinner');

let selectedFile = null;

// ===========================
// Event Listeners
// ===========================

// Upload box click
uploadBox.addEventListener('click', () => fileInput.click());

// File input change
fileInput.addEventListener('change', (e) => {
    const files = e.target.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// Remove button
removeBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    previewSection.style.display = 'none';
    analyzeBtn.disabled = true;
});

// Clear button
clearBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInput.value = '';
    previewSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    analyzeBtn.disabled = true;
});

// Analyze button
analyzeBtn.addEventListener('click', () => {
    if (selectedFile) {
        analyzeImage();
    }
});

// Close error button
closeErrorBtn.addEventListener('click', () => {
    errorSection.style.display = 'none';
});

// ===========================
// File Handling
// ===========================

function handleFileSelect(file) {
    // Validate file
    if (!CONFIG.ALLOWED_TYPES.includes(file.type)) {
        showError('Invalid file type. Please upload a JPEG or PNG image.');
        return;
    }

    if (file.size > CONFIG.MAX_FILE_SIZE) {
        showError('File size too large. Maximum size is 10MB.');
        return;
    }

    selectedFile = file;

    // Display preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileSize').textContent = formatFileSize(file.size);
        previewSection.style.display = 'block';
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';
        analyzeBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// ===========================
// Image Analysis
// ===========================

async function analyzeImage() {
    if (!selectedFile) return;

    // Show loading state
    analyzeBtn.disabled = true;
    spinner.style.display = 'inline-block';
    resultsSection.style.display = 'block';
    errorSection.style.display = 'none';

    const startTime = performance.now();

    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', selectedFile);

        // Send request to backend
        const response = await fetch(`${CONFIG.API_URL}/predict`, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed');
        }

        const result = await response.json();
        const endTime = performance.now();
        const analysisTime = ((endTime - startTime) / 1000).toFixed(2);

        // Display results
        displayResults(result, analysisTime);

    } catch (error) {
        console.error('Error:', error);
        resultsSection.style.display = 'none';
        showError(`Error: ${error.message || 'Failed to analyze image. Please make sure the backend server is running.'}`);
    } finally {
        analyzeBtn.disabled = false;
        spinner.style.display = 'none';
    }
}

function displayResults(result, analysisTime) {
    // Extract probabilities
    const tbPositive = result.tuberculosis_probability || 0;
    const tbNegative = result.normal_probability || 0;
    const prediction = result.prediction ;
    const model_version = result.model_version ;
    const confidence = Math.max(tbPositive, tbNegative) * 100;

    // Update result badge
    const resultBadge = document.getElementById('resultBadge');
    resultBadge.classList.remove('positive', 'negative');
    
    if (prediction.toLowerCase() === 'positive' || tbPositive > 0.5) {
        resultBadge.classList.add('positive');
        document.getElementById('resultLabel').textContent = '⚠️ Tuberculosis Positive';
    } else {
        resultBadge.classList.add('negative');
        document.getElementById('resultLabel').textContent = '✓ Tuberculosis Negative';
    }

    document.getElementById('resultConfidence').textContent = confidence.toFixed(1) + '%';

    // Update progress bars
    const tbPositivePercent = (tbPositive * 100).toFixed(1);
    const tbNegativePercent = (tbNegative * 100).toFixed(1);

    document.getElementById('tbPositiveBar').style.width = tbPositivePercent + '%';
    document.getElementById('tbPositiveText').textContent = tbPositivePercent + '%';

    document.getElementById('tbNegativeBar').style.width = tbNegativePercent + '%';
    document.getElementById('tbNegativeText').textContent = tbNegativePercent + '%';

    // Update details
    document.getElementById('analysisTime').textContent = analysisTime + 's';
    document.getElementById('modelVersion').textContent = model_version;
    document.getElementById('resultStatus').textContent = 'Complete';

    // Display Grad-CAM visualizations if available
    const visualizationSection = document.getElementById('visualizationSection');
    if (result.heatmap && result.overlayed_image) {
        document.getElementById('heatmapImage').src = result.heatmap;
        document.getElementById('overlayImage').src = result.overlayed_image;
        visualizationSection.style.display = 'block';
    } else {
        visualizationSection.style.display = 'none';
    }

    resultsSection.style.display = 'block';
}

// ===========================
// Error Handling
// ===========================

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorSection.style.display = 'block';
}

// ===========================
// Initialization
// ===========================

// Check if API is available
document.addEventListener('DOMContentLoaded', () => {
    checkAPIConnection();
});

async function checkAPIConnection() {
    try {
        const response = await fetch(`${CONFIG.API_URL}/health`, {
            method: 'GET'
        });
        if (response.ok) {
            console.log('Backend API is connected');
        }
    } catch (error) {
        console.warn('Backend API is not available. Make sure the FastAPI server is running at ' + CONFIG.API_URL);
    }
}
