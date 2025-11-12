from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import os
import tempfile
import shutil
from pathlib import Path
import logging
import base64
from io import BytesIO

from keras.models import load_model
import tensorflow as tf

from PIL import Image
import numpy as np
from time import time
import cv2

app = FastAPI(title="Lung TB Classifier API", version="1.0.0")

# Add CORS middleware - MUST be before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the correct model path relative to this file
# The structure is: Lung_project/backend/main.py
# Model is at: Lung_project/models/model_best_12.h5
# So we go up one level from backend/
current_dir = Path(__file__).parent.parent  # Go from backend/ to Lung_project/
model_path = current_dir / "models" / "model_best_12.h5"

# Check if model exists
if not model_path.exists():
    raise FileNotFoundError(f"Model not found at: {model_path}")

model = load_model(str(model_path))


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.info(f"Model loaded from: {model_path}")

# ===========================
# Grad-CAM Functions
# ===========================

def grad_cam_claude(model, image, class_idx, layer_name='conv2d'):
    """
    Generate Grad-CAM heatmap for a specific class prediction.
    """
    # Ensure image has correct dimensions
    if len(image.shape) == 2:
        image = image[np.newaxis, ..., np.newaxis]
    elif len(image.shape) == 3:
        image = image[np.newaxis, ...]
    
    # Cast image to float32
    image = tf.cast(image, tf.float32)
    
    # Create a model that outputs conv layer and predictions
    grad_model = tf.keras.Model(
        [model.inputs], 
        [model.get_layer(layer_name).output, model.output]
    )
    
    with tf.GradientTape() as tape:
        conv_output, predictions = grad_model(image)
        if class_idx is None:
            class_idx = tf.argmax(predictions[0])
        target = predictions[:, class_idx]

    # Get gradients
    grads = tape.gradient(target, conv_output)
    
    # Average gradients across spatial dimensions
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1))
    
    # Weight channels by gradients
    conv_output = conv_output[0]
    heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_output), axis=-1)
    
    # Apply ReLU and normalize
    heatmap = tf.maximum(heatmap, 0) / (tf.reduce_max(heatmap) + 1e-10)
    heatmap = heatmap.numpy()
    
    # Resize to original image size
    heatmap = cv2.resize(heatmap, (256, 256))
    
    return heatmap

def grad_cam(model, image, class_idx, layer_name='conv2d_1'):
    """
    Generate Grad-CAM heatmap for a specific class prediction.
    """
    # Ensure image has batch dimension and channel dimension
    if len(image.shape) == 2:
        image = image[np.newaxis, ..., np.newaxis]
    elif len(image.shape) == 3:
        image = image[np.newaxis, ...]
    
    # Cast image to float32
    image = tf.cast(image, tf.float32)
        
    # Get the score for target class
    with tf.GradientTape() as tape:
        tape.watch(image)  # Explicitly watch the input image
        # Get the target conv layer
        grad_model = tf.keras.Model(
            [model.inputs], 
            [model.get_layer(layer_name).output, model.output]
        )
        
        # Get conv output and predictions
        conv_output, predictions = grad_model(image)
        if class_idx is None:
            class_idx = tf.argmax(predictions[0])
        target = predictions[:, class_idx]

    # Get gradients
    grads = tape.gradient(target, conv_output)
    
    # Safe pooling operation
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1))
    
    # Weight the channels by corresponding gradients
    cam = tf.reduce_sum(tf.multiply(pooled_grads, conv_output[0]), axis=-1)
    
    # Apply ReLU and normalize
    cam = tf.maximum(cam, 0) / (tf.reduce_max(cam) + 1e-20)
    cam = cam.numpy()
    
    # Resize to original image size
    cam = cv2.resize(cam, (image.shape[1], image.shape[2]))

    heatmap_normalized = (cam * 255).astype(np.uint8)
    heatmap_colored = cv2.applyColorMap(heatmap_normalized, cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    
    return heatmap_colored

def create_overlayed_image(image, heatmap_colored, alpha=0.4):
    """
    Create an overlayed image with heatmap.
    
    Args:
        image: Original grayscale image (256x256, values 0-1)
        heatmap: Heatmap (256x256, values 0-1)
        alpha: Transparency factor
    
    Returns:
        Overlayed RGB image (256x256x3, values 0-255)
    """
    # Normalize image to 0-255
    image_normalized = (image * 255).astype(np.uint8)
    
    
    # Create overlay
    if len(image_normalized.shape) == 2:
        image_rgb = cv2.cvtColor(image_normalized, cv2.COLOR_GRAY2RGB)
    else:
        image_rgb = image_normalized
    
    overlayed = cv2.addWeighted(image_rgb, 1, heatmap_colored, alpha, 0)
    
    return overlayed

def image_to_base64(image_array):
    """
    Convert numpy image array to base64 string.
    """
    # Ensure values are in 0-255 range
    if image_array.dtype != np.uint8:
        image_array = (image_array * 255).astype(np.uint8)
    
    # Convert to PIL Image
    if len(image_array.shape) == 3:
        pil_image = Image.fromarray(image_array, 'RGB')
    else:
        pil_image = Image.fromarray(image_array, 'L')
    
    # Convert to base64
    buffer = BytesIO()
    pil_image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict tuberculosis from chest X-ray image.
    """
    start_time = time()
    
    try:
        # Validate file type
        allowed_extensions = {".png", ".jpg", ".jpeg"}
        file_extension = Path(file.filename).suffix.lower()

        if file_extension not in allowed_extensions:
            return {
                "error": "Invalid file type",
                "allowed_types": list(allowed_extensions),
                "status": "error"
            }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name
        
        try:
            # Load and preprocess image
            target = (256, 256)
            img = Image.open(temp_file_path)
            img = img.convert("L")
            img = np.array(img)

            y_size = img.shape[0]
            x_size = img.shape[1]
            border_gap = 16
            
            img = img[border_gap:y_size - border_gap,border_gap:x_size - border_gap]

            img = Image.fromarray((img).astype(np.uint8)) if img.dtype != np.uint8 else Image.fromarray(img)
            img = img.resize(target, resample=Image.BILINEAR)

            img_normalized = (np.array(img).astype(np.float32) / 255.0)
            img_batch = np.expand_dims(img_normalized, axis=-1)
            img_batch = np.expand_dims(img_batch, axis=0)

            # Make prediction (model.predict is not async)
            pred_prob = model.predict(img_batch, verbose=0)
            
            # Extract probabilities
            normal_prob = float(pred_prob[0][0])
            tb_prob = float(pred_prob[0][1])
            
            # Determine class
            pred_class = "Positive" if tb_prob > normal_prob else "Negative"
            predicted_class_idx = 1 if tb_prob > normal_prob else 0

            logger.info(f"Prediction: {pred_class} (TB: {tb_prob:.4f}, Normal: {normal_prob:.4f})")

            # Generate Grad-CAM
            try:
                # Find the last convolutional layer
                last_conv_layer = None
                for layer in model.layers:
                    if 'conv' in layer.name.lower():
                        last_conv_layer = layer.name
                
                if last_conv_layer:
                    heatmap = grad_cam(model, img_normalized, predicted_class_idx, layer_name=last_conv_layer)
                    overlayed_image = create_overlayed_image(img_normalized, heatmap, alpha=0.3)
                    
                    # Convert to base64
                    heatmap_base64 = image_to_base64(heatmap)
                    overlayed_base64 = image_to_base64(overlayed_image)
                else:
                    heatmap_base64 = None
                    overlayed_base64 = None
                    logger.warning("No convolutional layer found for Grad-CAM")
            except Exception as e:
                logger.error(f"Grad-CAM generation failed: {str(e)}")
                heatmap_base64 = None
                overlayed_base64 = None

            processing_time = (time() - start_time) * 1000  # in milliseconds
            logger.info(heatmap_base64)
            return {
                "prediction": pred_class,
                "tuberculosis_probability": round(tb_prob, 4),
                "normal_probability": round(normal_prob, 4),
                "processing_time_ms": round(processing_time, 2),
                "model_version": str(model_path).split("/")[-1].replace(".h5", ""),
                "status": "success",
                "heatmap": heatmap_base64,
                "overlayed_image": overlayed_base64
            }
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
    except Exception as e:
        processing_time = (time() - start_time) * 1000
        logger.error(f"Prediction error: {str(e)}")
        return {
            "error": str(e),
            "status": "error",
            "processing_time_ms": round(processing_time, 2)
        }



if __name__ == "__main__":
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    