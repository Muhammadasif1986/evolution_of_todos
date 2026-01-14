# Vercel Deployment - Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Go to Vercel
- Visit https://vercel.com
- Sign in with GitHub
- Click "Add New" → "Project"

### 2. Import Project
- Select "evolution_of_todos" repository
- Framework: `Next.js` (should auto-detect)
- Root Directory: `frontend`
- Click "Continue"

### 3. Add Environment Variable
- Name: `NEXT_PUBLIC_API_URL`
- Value: `https://your-backend-api.com` (your actual backend URL)
- Environment: Production
- Click "Deploy"

### 4. Wait for Deployment
- Vercel will build and deploy
- Takes 2-5 minutes
- Get your URL: `https://your-project.vercel.app`

### 5. Verify
- Open your URL
- CSS should load ✅
- No build warnings ✅
- API calls should work ✅

## 📝 What's Fixed

| Issue | Fix |
|-------|-----|
| CSS not loading | ✅ Vercel config updated |
| Build warnings | ✅ Removed deprecated `builds` |
| Fast deployment | ✅ Added .vercelignore |

## 🔧 Configuration Files Used

- `frontend/vercel.json` - Updated to modern format
- `vercel.json` - Root config for monorepo
- `frontend/.vercelignore` - Exclude unnecessary files

## 🚀 After Deployment

- Frontend URL: `https://your-app.vercel.app`
- Backend URL: Must be set in env variable
- Both must communicate (check CORS if API calls fail)

## ❓ If Issues Arise

1. **CSS still not loading?**
   - Clear Vercel build cache (Project Settings → Build Cache → Clear All)
   - Redeploy

2. **API calls failing?**
   - Check `NEXT_PUBLIC_API_URL` is set correctly
   - Verify backend CORS allows your Vercel domain
   - Check backend is running

3. **Build still warnings?**
   - Verify `frontend/vercel.json` was updated
   - Hard refresh browser (Ctrl+Shift+R)

## 📖 Full Guide

See `VERCEL_DEPLOYMENT_GUIDE.md` for comprehensive documentation.

---

**Status:** ✅ Ready to Deploy
**Last Updated:** 2026-01-09
