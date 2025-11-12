# Deployment Guide - Lung TB Classifier

Choose the deployment option that best fits your needs.

---

## ⭐ Option 1: Render (SIMPLEST - Recommended for Beginners)

### Pros:
- ✅ Free tier available
- ✅ Automatic GitHub deployment
- ✅ SSL certificate included
- ✅ Very easy setup

### Steps:

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy TB classifier"
   git push origin practical_statistics
   ```

2. **Create Render Account:**
   - Go to https://render.com
   - Sign up with GitHub

3. **Deploy Backend:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port 8000`
   - Set environment variables if needed
   - Click Deploy

4. **Deploy Frontend:**
   - Click "New +" → "Static Site"
   - Connect same GitHub repository
   - Build command: (leave empty or `echo "No build needed"`)
   - Publish directory: `Lung_project/frontend`
   - Click Deploy

5. **Update Frontend API URL:**
   - Once backend is deployed, get the URL (e.g., `https://tb-classifier.onrender.com`)
   - Update `Lung_project/frontend/script.js`:
     ```javascript
     const CONFIG = {
         API_URL: 'https://tb-classifier.onrender.com',
         MAX_FILE_SIZE: 10 * 1024 * 1024,
         ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/jpg']
     };
     ```
   - Commit and push

**Cost:** Free (with limitations) or $7/month per service

---

## 🚀 Option 2: Heroku (Easy Alternative)

### Pros:
- ✅ Simple deployment
- ✅ GitHub integration
- ✅ Good documentation

### Steps:

1. **Create `requirements.txt`:**
   ```bash
   cd /Users/nurma/vscode_projects/data_projects
   pip freeze > requirements.txt
   ```

2. **Create `Procfile` in `Lung_project/backend/`:**
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **Create Heroku Account:**
   - Go to https://www.heroku.com
   - Sign up

4. **Install Heroku CLI:**
   ```bash
   brew install heroku/brew/heroku  # macOS
   heroku login
   ```

5. **Deploy:**
   ```bash
   cd Lung_project/backend
   heroku create your-app-name
   git push heroku main
   ```

6. **Update Frontend API URL** in `script.js`

**Cost:** Free tier removed, paid plans start at $5/month

---

## ☁️ Option 3: AWS (More Control)

### Using EC2 + S3:

1. **Create AWS Account** at https://aws.amazon.com

2. **Launch EC2 Instance:**
   - Choose Ubuntu 22.04 LTS
   - Instance type: t3.micro (free tier eligible)
   - Create security group (allow HTTP, HTTPS, SSH)

3. **SSH into Instance:**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

4. **Install Dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv
   cd /home/ubuntu
   git clone your-repo-url
   cd your-repo
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Run Backend:**
   ```bash
   cd Lung_project/backend
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

6. **Deploy Frontend to S3:**
   - Create S3 bucket
   - Upload files from `Lung_project/frontend`
   - Enable static website hosting
   - Update API URL in `script.js`

**Cost:** Free tier (1 year), then ~$5-10/month

---

## 🐳 Option 4: Docker + Fly.io (Scalable)

### Create Docker Setup:

1. **Create `Dockerfile` in `Lung_project/backend/`:**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Create `.dockerignore`:**
   ```
   __pycache__
   *.pyc
   .git
   .env
   venv/
   ```

3. **Deploy to Fly.io:**
   ```bash
   # Install Fly CLI
   curl -L https://fly.io/install.sh | sh
   
   cd Lung_project/backend
   flyctl launch
   flyctl deploy
   ```

**Cost:** Free tier available, paid starts at $5/month

---

## 📋 Quick Comparison

| Option | Ease | Cost | Free Tier | Speed |
|--------|------|------|-----------|-------|
| **Render** | ⭐⭐⭐⭐⭐ | $0-7/mo | Yes | Fast |
| **Heroku** | ⭐⭐⭐⭐ | $5+/mo | No | Good |
| **AWS** | ⭐⭐⭐ | $0-10/mo | Yes | Very Fast |
| **Fly.io** | ⭐⭐⭐⭐ | $0+/mo | Yes | Very Fast |
| **DigitalOcean** | ⭐⭐⭐ | $5+/mo | No | Fast |

---

## Pre-Deployment Checklist

### 1. Create `requirements.txt`:
```bash
cd /Users/nurma/vscode_projects/data_projects
pip freeze > requirements.txt
```

Should include:
```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
tensorflow>=2.13.0
Pillow>=10.0.0
numpy>=1.24.0
```

### 2. Create `.gitignore`:
```
__pycache__/
*.pyc
*.pyo
*.egg-info/
.env
.venv
venv/
model_best_*.h5
*.sqlite
.DS_Store
```

### 3. Move Model Files:
The model file is large (~100+ MB). Options:
- **A) Upload to cloud storage** (AWS S3, Google Cloud Storage)
  ```python
  # In main.py
  import boto3
  s3 = boto3.client('s3')
  s3.download_file('bucket-name', 'model_best_12.h5', 'model_best_12.h5')
  model = load_model('model_best_12.h5')
  ```

- **B) Use Git LFS** (Large File Storage):
  ```bash
  git lfs install
  git lfs track "*.h5"
  git add .gitattributes
  git add *.h5
  git commit -m "Add model files with LFS"
  ```

- **C) Download on startup** (simplest for free tier):
  ```python
  # In main.py
  import urllib.request
  if not os.path.exists('model_best_12.h5'):
      urllib.request.urlretrieve(
          'https://your-cloud-url/model_best_12.h5',
          'model_best_12.h5'
      )
  model = load_model('model_best_12.h5')
  ```

### 4. Test Locally First:
```bash
# Terminal 1
cd Lung_project/backend
python main.py

# Terminal 2
cd Lung_project/frontend
python3 -m http.server 8080

# Then test at http://localhost:8080
```

### 5. Environment Variables:
Create `.env` for sensitive data:
```
MODEL_PATH=model_best_12.h5
ENVIRONMENT=production
```

Update `main.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
model_path = os.getenv('MODEL_PATH', 'model_best_12.h5')
```

---

## Recommended Deployment Path

**For Beginners:**
1. Start with **Render** (easiest)
2. Deploy backend first
3. Deploy frontend second
4. Test and iterate

**For Production:**
1. Use **AWS** or **Fly.io**
2. Set up CI/CD pipeline
3. Add monitoring and logging
4. Use custom domain (e.g., tb-classifier.com)

---

## Custom Domain Setup

1. **Buy Domain:**
   - Namecheap, GoDaddy, Google Domains, etc.

2. **Point to Your Deployment:**
   - Render: Add custom domain in settings
   - AWS: Use Route 53
   - Fly.io: Add CNAME record

3. **Get SSL Certificate:**
   - Most platforms provide free SSL
   - Or use Let's Encrypt

---

## Monitoring & Logging

After deployment, monitor your app:

**Render:**
- Built-in logs in dashboard
- Error notifications

**AWS CloudWatch:**
- Real-time monitoring
- Performance metrics

**Fly.io:**
- `flyctl logs` command
- Real-time streaming

---

## Final Tips

✅ **Always test locally first**  
✅ **Keep model file size in mind**  
✅ **Use environment variables for secrets**  
✅ **Monitor API usage and costs**  
✅ **Set up automated backups**  
✅ **Add rate limiting to prevent abuse**  
✅ **Keep dependencies updated**  

---

## Need Help?

- **Render Docs:** https://render.com/docs
- **FastAPI Deploy:** https://fastapi.tiangolo.com/deployment/
- **AWS Free Tier:** https://aws.amazon.com/free/
- **Fly.io Docs:** https://fly.io/docs/

---

**Next Steps:**
1. Choose your deployment platform
2. Follow the setup instructions
3. Test your deployed app
4. Share with users!

Good luck! 🚀
