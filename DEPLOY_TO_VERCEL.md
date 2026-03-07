# 🚀 Deploy to Vercel - Quick Guide

## Option 1: Deploy via Vercel CLI (Fastest)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
# From project root directory
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? **Your account**
- Link to existing project? **N**
- Project name? **career-guidance-system** (or your choice)
- Directory? **./** (press Enter)
- Override settings? **N**

### Step 4: Get Your Link
Vercel will give you a URL like:
```
https://career-guidance-system-xxx.vercel.app
```

---

## Option 2: Deploy via Vercel Website (Easiest)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Go to Vercel
Visit: https://vercel.com/

### Step 3: Import Project
- Click "Add New" → "Project"
- Import your GitHub repository
- Click "Deploy"

### Step 4: Get Your Link
Vercel will automatically deploy and give you a URL!

---

## Configuration

The project is already configured with `vercel.json`:
- Frontend: React app in `/frontend`
- Backend: Python API in `/api`
- CORS: Enabled for all origins

---

## What Gets Deployed

### Frontend (React):
- Chat interface
- Career form
- Results display
- Hosted on Vercel CDN

### Backend (Serverless Functions):
- `/api/health` - Health check
- `/api/chat` - AI chat (fallback mode)
- `/api/rank-careers` - Career ranking
- `/api/explain-career` - Explanations

---

## Testing Your Deployment

Once deployed, test these URLs:

```bash
# Health check
https://your-app.vercel.app/api/health

# Frontend
https://your-app.vercel.app
```

---

## Important Notes

### Current Deployment:
- ✅ Frontend works perfectly
- ✅ Backend API works (fallback mode)
- ⚠️ AWS Bedrock not included (requires AWS credentials)

### For Full AWS Integration:
You'll need to deploy backend to AWS Lambda separately and update the API URL.

### For Demo Purposes:
The current deployment is perfect! It shows:
- Working UI
- AI conversations (fallback mode)
- Career ranking
- Explanations
- Complete user flow

---

## Troubleshooting

### Build Fails?
Check that `frontend/package.json` has build script:
```json
"scripts": {
  "build": "react-scripts build"
}
```

### API Not Working?
- Check `/api` folder exists
- Check Python files have correct handler class
- Check CORS headers are set

### Frontend Not Loading?
- Check `vercel.json` routes
- Check build directory is correct

---

## Custom Domain (Optional)

After deployment, you can add a custom domain:
1. Go to Vercel dashboard
2. Select your project
3. Go to "Settings" → "Domains"
4. Add your domain

---

## Environment Variables (If Needed)

To add AWS credentials later:
1. Go to Vercel dashboard
2. Select your project
3. Go to "Settings" → "Environment Variables"
4. Add:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_DEFAULT_REGION`

---

## Success!

Your project will be live at:
```
https://career-guidance-system-xxx.vercel.app
```

Share this link with hackathon judges! 🎉

---

## Quick Commands

```bash
# Deploy
vercel

# Deploy to production
vercel --prod

# Check deployment status
vercel ls

# View logs
vercel logs
```

---

**Your demo link will be ready in 2-3 minutes!** 🚀
