# Deployment Guide

## Prerequisites
- MongoDB Atlas account (free tier)
- Render account (for backend deployment)

---

## Step 1: Prepare for Deployment

### Create `render.yaml` (optional)
This file helps Render auto-configure your service.

```yaml
services:
  - type: web
    name: search-engine-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: MONGODB_URL
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_NAME
        value: search_engine_db
      - key: ALGORITHM
        value: HS256
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: 30
      - key: DEBUG
        value: False
      - key: ALLOWED_ORIGINS
        value: "*"
```

---

## Step 2: Deploy to Render

### Option A: Deploy via GitHub

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Create Render Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: search-engine-api
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables**
   - `MONGODB_URL`: Your MongoDB Atlas connection string
   - `SECRET_KEY`: Generate a secure random string
   - `DATABASE_NAME`: search_engine_db
   - `DEBUG`: False
   - `ALLOWED_ORIGINS`: * (or your frontend URL)

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your API will be live at: `https://your-app-name.onrender.com`

### Option B: Deploy via Render CLI

```bash
# Install Render CLI
pip install render-cli

# Login
render login

# Deploy
render deploy
```

---

## Step 3: Test Deployed API

### Test Health Endpoint
```bash
curl https://your-app-name.onrender.com/health
```

### Test API Documentation
Visit: `https://your-app-name.onrender.com/docs`

### Test Authentication
```bash
# Signup
curl -X POST https://your-app-name.onrender.com/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123"}'

# Login
curl -X POST https://your-app-name.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

---

## Alternative Platforms

### Railway
1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub
3. Add environment variables
4. Deploy automatically

### Heroku
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
3. Deploy:
   ```bash
   heroku create
   heroku config:set MONGODB_URL=<your-url>
   git push heroku main
   ```

---

## Production Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user created with strong password
- [ ] Network access configured
- [ ] Environment variables set in Render
- [ ] SECRET_KEY is strong and random
- [ ] DEBUG set to False
- [ ] ALLOWED_ORIGINS configured properly
- [ ] API deployed and accessible
- [ ] Health check endpoint working
- [ ] Authentication tested
- [ ] Document upload tested
- [ ] Search functionality tested

---

## Monitoring

### Check Logs
- Render Dashboard → Your Service → Logs
- Look for startup messages and errors

### Health Checks
Render automatically monitors your `/health` endpoint

---

## Troubleshooting

### MongoDB Connection Issues
- Verify connection string is correct
- Check MongoDB Atlas network access allows Render IPs
- Ensure database user has correct permissions

### Deployment Fails
- Check build logs for errors
- Verify all dependencies in requirements.txt
- Ensure Python version compatibility

### API Not Responding
- Check if service is running in Render dashboard
- Verify PORT environment variable is used
- Check logs for runtime errors
