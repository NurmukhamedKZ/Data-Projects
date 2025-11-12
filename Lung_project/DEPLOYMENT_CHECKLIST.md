# ✅ Deployment Checklist

Complete this checklist before and during deployment.

---

## 📋 Pre-Deployment (Do This First)

### Code & Files
- [ ] All code committed to Git
- [ ] `requirements.txt` created with all dependencies
- [ ] `.gitignore` configured (ignore __pycache__, .env, etc.)
- [ ] Model file included (`model_best_12.h5`)
- [ ] No sensitive data in code (API keys, passwords)

### Backend
- [ ] `Lung_project/backend/main.py` contains:
  - [ ] CORS middleware configured
  - [ ] `/health` endpoint working
  - [ ] `/predict` endpoint working
  - [ ] Proper error handling
- [ ] Model loads successfully
- [ ] Tested locally on `http://localhost:8000/docs`

### Frontend
- [ ] `Lung_project/frontend/index.html` created
- [ ] `Lung_project/frontend/styles.css` created
- [ ] `Lung_project/frontend/script.js` created
- [ ] Tested locally on `http://localhost:8080`
- [ ] Image upload works
- [ ] API calls work with local backend

### Testing
- [ ] Uploaded test image locally
- [ ] Got correct prediction
- [ ] No console errors in browser
- [ ] Responsive design works on mobile
- [ ] All buttons functional

---

## 🚀 Render Deployment Checklist

### Create Render Account
- [ ] Go to https://render.com
- [ ] Sign up with GitHub
- [ ] Authorize Render to access repositories
- [ ] Verify email

### Deploy Backend Service
- [ ] Click "New +" → "Web Service"
- [ ] Connect to `Data-Projects` repository
- [ ] Fill in service details:
  - [ ] Name: `tb-classifier-backend`
  - [ ] Environment: `Python 3`
  - [ ] Region: Closest to you
  - [ ] Build command: `pip install -r requirements.txt`
  - [ ] Start command: `cd Lung_project/backend && uvicorn main:app --host 0.0.0.0 --port 8000`
- [ ] Choose Free plan
- [ ] Click "Create Web Service"
- [ ] Wait 2-3 minutes for build
- [ ] Check logs for errors
- [ ] Copy backend URL (e.g., `https://tb-classifier-backend.onrender.com`)
- [ ] Test health endpoint: `[URL]/health`

### Deploy Frontend Service
- [ ] Click "New +" → "Static Site"
- [ ] Connect to same `Data-Projects` repository
- [ ] Fill in service details:
  - [ ] Name: `tb-classifier-frontend`
  - [ ] Build command: `echo "No build needed"` (or leave empty)
  - [ ] Publish directory: `Lung_project/frontend`
- [ ] Click "Create Static Site"
- [ ] Wait for deployment
- [ ] Copy frontend URL (e.g., `https://tb-classifier-frontend.onrender.com`)
- [ ] Test that site loads in browser

### Update Configuration
- [ ] Note your backend URL from Render
- [ ] Edit `Lung_project/frontend/script.js`
- [ ] Update `CONFIG.API_URL`:
  ```javascript
  API_URL: 'https://tb-classifier-backend.onrender.com'
  ```
- [ ] Save file
- [ ] Commit and push:
  ```bash
  git add Lung_project/frontend/script.js
  git commit -m "Update API URL for production"
  git push origin practical_statistics
  ```
- [ ] Wait for Render to auto-redeploy frontend (2-3 min)

---

## ✅ Post-Deployment Testing

### Frontend Testing
- [ ] Open frontend URL in browser
- [ ] Page loads without errors
- [ ] UI looks correct
- [ ] Upload box appears
- [ ] Can click to select file

### Backend Testing
- [ ] Open Swagger UI: `[backend-url]/docs`
- [ ] Try health endpoint
- [ ] Try uploading image through Swagger

### End-to-End Testing
- [ ] Upload image through frontend
- [ ] See loading spinner
- [ ] Get prediction results
- [ ] Check confidence scores
- [ ] Verify processing time shown

### Error Handling
- [ ] Try invalid file type (should show error)
- [ ] Try very large file (should show error)
- [ ] Check browser console for errors
- [ ] Check Render logs for backend errors

---

## 📊 Monitoring After Launch

### Daily
- [ ] Check frontend loads
- [ ] Test prediction once
- [ ] Verify no error messages

### Weekly
- [ ] Check Render dashboard logs
- [ ] Monitor resource usage
- [ ] Test with different images
- [ ] Get user feedback

### Monthly
- [ ] Review prediction accuracy
- [ ] Check for errors in logs
- [ ] Monitor costs
- [ ] Plan improvements

---

## 🐛 Common Issues & Fixes

### Issue: CORS Error in Console
**Checklist:**
- [ ] Backend URL is correct in script.js
- [ ] Backend has CORS middleware
- [ ] API_URL doesn't have trailing slash
- [ ] Check browser console for exact error
- [ ] Wait 5 min for auto-redeploy

**Fix:**
```javascript
// Check this in script.js
API_URL: 'https://tb-classifier-backend.onrender.com',  // ✅ Correct
API_URL: 'https://tb-classifier-backend.onrender.com/',  // ❌ Wrong (extra slash)
```

### Issue: Model File Not Found
**Checklist:**
- [ ] `model_best_12.h5` is in Lung_project/ directory
- [ ] File is committed to Git
- [ ] File name matches in main.py

**Fix:**
```bash
ls -la Lung_project/ | grep model
# Should show: model_best_12.h5
```

### Issue: Backend Doesn't Respond
**Checklist:**
- [ ] Backend service is running on Render (green status)
- [ ] Build completed without errors
- [ ] Check Render logs for error messages
- [ ] Restart service: Render Dashboard → Service → Restart

### Issue: Slow Responses (>5 sec)
**Checklist:**
- [ ] Free tier may be limited
- [ ] Model loading takes time on first request
- [ ] Check Render logs for performance

**Solution:**
- [ ] Upgrade to paid tier ($7/month)
- [ ] Implement model caching

---

## 📝 Documentation Checklist

- [ ] `README_DEPLOY.md` - Complete guide
- [ ] `QUICK_START.md` - Overview
- [ ] `RENDER_DEPLOY.md` - Step-by-step for Render
- [ ] `DEPLOYMENT.md` - All platform options
- [ ] `SETUP.md` - Local development
- [ ] `VISUAL_GUIDE.md` - Visual diagrams
- [ ] This checklist - Track progress

---

## 🎉 Successful Deployment Indicators

You'll know everything works when:

✅ **Frontend loads** - No errors in console  
✅ **Can upload images** - File dialog appears  
✅ **API responds** - Prediction returns in 2-5 seconds  
✅ **Results display** - Confidence scores shown  
✅ **URLs shared** - Friends can access your app  
✅ **No errors** - Render logs show success  

---

## 📋 Final Sign-Off

- [ ] Backend deployed and working
- [ ] Frontend deployed and working
- [ ] API URL updated in frontend
- [ ] End-to-end testing passed
- [ ] Errors resolved
- [ ] Ready to share with users
- [ ] Documentation complete

---

## 🚀 Deployment Complete!

Your Lung TB Classifier is now live on the internet!

**Frontend URL:** https://[your-frontend].onrender.com  
**Backend URL:** https://[your-backend].onrender.com  
**API Docs:** https://[your-backend].onrender.com/docs

Share these URLs with users, colleagues, or professors to showcase your project!

---

## Next Steps

1. ✅ Share URLs on social media
2. ✅ Add to your portfolio
3. ✅ Gather feedback from users
4. ✅ Monitor performance
5. ✅ Plan improvements
6. ✅ Consider production deployment

---

**Congratulations! 🎊 You've successfully deployed a machine learning application!**
