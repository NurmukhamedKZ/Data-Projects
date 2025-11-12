# Lung TB Classifier - Complete Setup Guide

## Issues Fixed

✅ **CORS Error Fixed** - Added proper CORS middleware to backend  
✅ **Model Loading** - Removed `await` from `model.predict()` (Keras is sync)  
✅ **Probability Calculation** - Fixed duplicate `pred_prob[0][1]` bug  
✅ **Frontend Configuration** - API URL already set correctly  

## Setup Instructions

### Step 1: Install Dependencies

Run from the project root:

```bash
cd /Users/nurma/vscode_projects/data_projects

# Install required packages
uv add fastapi uvicorn python-multipart tensorflow pillow numpy

# Or if using pip:
pip install fastapi uvicorn python-multipart tensorflow pillow numpy
```

### Step 2: Start Backend (Terminal 1)

```bash
cd /Users/nurma/vscode_projects/data_projects/Lung_project/backend

# Run the backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test the API:**
- Visit: `http://localhost:8000/docs` for interactive API docs
- Or test health check: `http://localhost:8000/health`

### Step 3: Start Frontend (Terminal 2)

```bash
cd /Users/nurma/vscode_projects/data_projects/Lung_project/frontend

# Start local web server
python3 -m http.server 8080
```

You should see:
```
Serving HTTP on 0.0.0.0 port 8080
```

### Step 4: Open in Browser

- Frontend: `http://localhost:8080`
- Backend API Docs: `http://localhost:8000/docs`

## What Works Now

✨ **Frontend:**
- Upload image via drag & drop or click
- See image preview
- Click "Analyze Image"
- Get TB prediction with confidence scores

✨ **Backend:**
- Accepts image files (PNG, JPG, JPEG)
- Preprocesses image to 256x256 grayscale
- Loads model: `model_best_12.h5`
- Returns JSON with:
  - `prediction`: "Positive" or "Negative"
  - `tuberculosis_probability`: 0.0-1.0
  - `normal_probability`: 0.0-1.0
  - `processing_time_ms`: float
  - `model_version`: "model_best_12.h5"
  - `status`: "success" or "error"

## Example Response

```json
{
  "prediction": "Positive",
  "tuberculosis_probability": 0.8542,
  "normal_probability": 0.1458,
  "processing_time_ms": 245.32,
  "model_version": "model_best_12.h5",
  "status": "success"
}
```

## Troubleshooting

### CORS Error
**Problem:** "Cross-Origin Request Blocked"  
**Solution:** Make sure backend is running and CORS middleware is configured (now fixed)

### Model Not Found
**Problem:** "No such file or directory: 'Lung_project/model_best_12.h5'"  
**Solution:** Make sure you're running from the correct directory or update the path in `main.py`

### Port Already in Use
**Problem:** "Address already in use"  
**Solution:** 
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Or use different port:
python main.py --port 8001
```

### Connection Refused
**Problem:** "Error: Failed to analyze image. Backend is not running"  
**Solution:** Make sure backend is started in Terminal 1

## Development Notes

- Frontend is a vanilla JS application (no build needed)
- Backend uses FastAPI with async support
- Model is loaded once at startup for performance
- Images are temporarily stored during processing and cleaned up
- CORS is enabled to allow cross-origin requests from frontend

## Next Steps

1. Test with actual lung X-ray images
2. Monitor model performance
3. Consider adding image preprocessing enhancements
4. Add database to store predictions
5. Deploy to production with proper authentication

## Production Deployment

For production:
1. Change `allow_origins=["*"]` to specific domain
2. Set `reload=False` in uvicorn.run()
3. Use proper error logging
4. Add rate limiting
5. Use HTTPS
6. Deploy on cloud platform (AWS, GCP, Azure, etc.)
