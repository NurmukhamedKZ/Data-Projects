from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import os
import tempfile
import shutil
from pathlib import Path
import logging

from keras.models import load_model

from PIL import Image
import numpy as np
from time import time

app = FastAPI(title="Lung TB Classifier API", version="1.0.0")

# Add CORS middleware - MUST be before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = "Lung_project/models/model_best_12.h5"
model = load_model(model_path)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
            img = img.resize(target, resample=Image.BILINEAR)
            img = np.array(img).astype(np.float32) / 255.0
            img = np.expand_dims(img, axis=-1)
            img = np.expand_dims(img, axis=0)

            # Make prediction (model.predict is not async)
            pred_prob = model.predict(img, verbose=0)
            
            # Extract probabilities
            normal_prob = float(pred_prob[0][0])
            tb_prob = float(pred_prob[0][1])
            
            # Determine class
            pred_class = "Positive" if tb_prob > normal_prob else "Negative"

            logger.info(f"Prediction: {pred_class} (TB: {tb_prob:.4f}, Normal: {normal_prob:.4f})")

            processing_time = (time() - start_time) * 1000  # in milliseconds
            return {
                "prediction": pred_class,
                "tuberculosis_probability": round(tb_prob, 4),
                "normal_probability": round(normal_prob, 4),
                "processing_time_ms": round(processing_time, 2),
                "model_version": model_path.split("/")[-1].replace(".h5", ""),
                "status": "success"
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
    