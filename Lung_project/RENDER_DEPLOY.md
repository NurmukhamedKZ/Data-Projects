# Quick Deployment Guide for Render.com

## Step-by-Step Deployment (5 minutes)

### 1. Prepare Your Code
Make sure everything is committed to GitHub:

```bash
cd /Users/nurma/vscode_projects/data_projects
git add .
git commit -m "Ready for deployment"
git push origin practical_statistics
```

### 2. Create Render Account
- Visit https://render.com
- Click "Sign up"
- Choose "Sign up with GitHub"
- Authorize Render to access your repositories

### 3. Deploy Backend

**Part A: Create Web Service**
1. Click "New +" button
2. Select "Web Service"
3. Select your Data-Projects repository
4. Fill in the form:
   - Name: `tb-classifier-backend`
   - Environment: `Python 3`
   - Region: Choose closest to you
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd Lung_project/backend && uvicorn main:app --host 0.0.0.0 --port 8000`
   - Plan: Free (Free tier)

5. Click "Create Web Service"
6. Wait 2-3 minutes for deployment
7. Copy your backend URL (e.g., `https://tb-classifier-backend.onrender.com`)

### 4. Deploy Frontend

**Part B: Create Static Site**
1. Click "New +" button
2. Select "Static Site"
3. Select your Data-Projects repository
4. Fill in the form:
   - Name: `tb-classifier-frontend`
   - Build Command: `echo "No build needed"`
   - Publish directory: `Lung_project/frontend`

5. Click "Create Static Site"
6. Wait for deployment
7. Copy your frontend URL (e.g., `https://tb-classifier-frontend.onrender.com`)

### 5. Update Frontend Configuration

Now you need to update the frontend to use the deployed backend URL:

1. In VS Code, open: `Lung_project/frontend/script.js`
2. Find line 2-5:
   ```javascript
   const CONFIG = {
       API_URL: 'http://localhost:8000',
   ```

3. Replace with your Render backend URL:
   ```javascript
   const CONFIG = {
       API_URL: 'https://tb-classifier-backend.onrender.com',
   ```

4. Save the file
5. Commit and push:
   ```bash
   git add Lung_project/frontend/script.js
   git commit -m "Update API URL for production"
   git push origin practical_statistics
   ```

6. Render will auto-redeploy the frontend

### 6. Test Your Deployment

1. Visit your frontend URL: `https://tb-classifier-frontend.onrender.com`
2. Try uploading an image
3. See your predictions!

---

## Troubleshooting

### Backend not responding
- Check Render dashboard logs
- Make sure `model_best_12.h5` is in the repository
- Check if the model file path is correct

### CORS errors
- Backend CORS is already configured
- Make sure you updated the API_URL in script.js
- Wait 5 minutes for Render to fully redeploy

### Model too slow to load
- Free tier has limited memory
- Consider upgrading to paid plan
- Or implement lazy loading

---

## Environment Variables (Optional)

If you need to set environment variables:

1. In Render dashboard, go to Service > Environment
2. Click "Add Environment Variable"
3. Add variables like:
   - `ENVIRONMENT=production`
   - `DEBUG=false`

---

## Custom Domain (Optional)

To add your own domain:

1. Buy a domain (Namecheap, GoDaddy, etc.)
2. In Render dashboard: Settings > Custom Domain
3. Follow Render's DNS setup instructions
4. Usually takes 5-30 minutes to propagate

---

## Monitor Your Deployment

**Check Logs:**
1. Go to Render Dashboard
2. Click on your service
3. Click "Logs" tab
4. See real-time logs

**Monitor Performance:**
- Render shows request count
- Response times
- Memory usage
- Restart info

---

## Estimated Costs

**Free Tier:**
- 0.5 GB RAM
- Limited to 750 hours/month per service
- Pauses after 15 minutes inactivity
- Good for testing

**Paid Tier:**
- Starts at $7/month per service
- Full uptime
- Auto-restart on crashes
- Better performance

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Create Render account
3. ✅ Deploy backend service
4. ✅ Deploy frontend service
5. ✅ Update API URL in frontend
6. ✅ Test your app!

---

**Your URLs will be:**
- Backend: `https://tb-classifier-backend.onrender.com`
- Frontend: `https://tb-classifier-frontend.onrender.com`

You can share the frontend URL with anyone to use your app! 🎉
