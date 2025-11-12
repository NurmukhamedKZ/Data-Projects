# Lung Tuberculosis Classifier - Frontend

A modern, responsive web application for detecting tuberculosis from lung X-ray images using machine learning.

## Features

✨ **Clean & Modern UI**
- Professional gradient design
- Responsive layout (works on mobile, tablet, desktop)
- Smooth animations and transitions
- Intuitive user experience

📸 **Image Upload**
- Drag-and-drop support
- File validation
- Image preview
- Size limit protection (10MB max)

🤖 **AI Analysis**
- Real-time predictions
- Confidence scores
- Visual progress indicators
- Processing time tracking

⚠️ **Medical Disclaimer**
- Clear warning that this is for research purposes
- Not a substitute for professional medical diagnosis

## Technology Stack

- **HTML5** - Structure
- **CSS3** - Styling with modern features (flexbox, gradients, animations)
- **Vanilla JavaScript** - No dependencies required
- **Fetch API** - Backend communication

## Setup Instructions

### Frontend Only (What's in this folder)

1. **Start a local web server** (choose one):

   **Using Python:**
   ```bash
   # Python 3
   python3 -m http.server 8080
   
   # Python 2
   python -m SimpleHTTPServer 8080
   ```

   **Using Node.js:**
   ```bash
   npx http-server
   ```

   **Using PHP:**
   ```bash
   php -S localhost:8080
   ```

2. **Open in browser:**
   ```
   http://localhost:8080
   ```

### Backend Setup (FastAPI)

Your backend should be a FastAPI application with the following endpoint:

```python
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict tuberculosis from lung X-ray image.
    
    Expected return format:
    {
        "prediction": "Positive" or "Negative",
        "tuberculosis_probability": float (0.0 to 1.0),
        "model_version": str
    }
    """
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Preprocess image
        image = image.resize((256, 256))
        image_array = np.array(image) / 255.0
        
        # Add batch dimension if needed
        if len(image_array.shape) == 2:
            image_array = image_array[..., np.newaxis]
        elif len(image_array.shape) == 3:
            if image_array.shape[2] == 3:  # RGB to grayscale
                image_array = np.mean(image_array, axis=2, keepdims=True)
        
        image_array = image_array[np.newaxis, ...]
        
        # Make prediction with your model
        # prediction = model.predict(image_array)
        # tb_probability = prediction[0][0]  # Adjust based on your model output
        
        # For testing, you can use a dummy prediction:
        tb_probability = np.random.random()
        
        return {
            "prediction": "Positive" if tb_probability > 0.5 else "Negative",
            "tuberculosis_probability": float(tb_probability),
            "model_version": "1.0"
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"detail": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Running Both Frontend and Backend

1. **Terminal 1 - Start Backend (FastAPI):**
   ```bash
   cd /path/to/backend
   python main.py
   # or
   uvicorn main:app --reload
   ```

2. **Terminal 2 - Start Frontend:**
   ```bash
   cd /path/to/frontend
   python3 -m http.server 8080
   ```

3. **Open in browser:**
   ```
   http://localhost:8080
   ```

## Configuration

Edit `script.js` to change the API endpoint:

```javascript
const CONFIG = {
    API_URL: 'http://localhost:8000',  // Change this to your backend URL
    MAX_FILE_SIZE: 10 * 1024 * 1024,   // Max file size
    ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/jpg']
};
```

## File Structure

```
frontend/
├── index.html       # Main HTML file
├── styles.css       # Styling
├── script.js        # JavaScript functionality
└── README.md        # This file
```

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## API Response Format

The backend should return JSON in this format:

```json
{
    "prediction": "Positive",
    "tuberculosis_probability": 0.85,
    "model_version": "1.0"
}
```

- `prediction`: "Positive" or "Negative"
- `tuberculosis_probability`: Float between 0.0 and 1.0
- `model_version`: String (optional)

## Notes

- The application uses CORS-enabled communication with the backend
- File size is limited to 10MB for performance
- Only JPEG and PNG images are supported
- All medical disclaimers should be clearly displayed to users

## License

Educational and research purposes only.

## Support

For issues or questions, please refer to the backend implementation and ensure:
1. FastAPI server is running on the configured port
2. CORS is properly enabled on the backend
3. The `/predict` endpoint returns the expected JSON format
