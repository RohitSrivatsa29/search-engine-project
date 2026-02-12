# Quick Start Guide

## 🚀 Getting Started

### 1. Install Dependencies
```bash
cd f:\search-engine-project
pip install -r requirements.txt
```

✅ **Status**: Dependencies installed!

---

### 2. Set Up MongoDB

You have two options:

#### Option A: MongoDB Atlas (Recommended - Free Cloud)
1. Follow the guide in `MONGODB_SETUP.md`
2. Get your connection string
3. Update `.env` file with your MongoDB Atlas URL

#### Option B: Local MongoDB
1. Install MongoDB locally
2. Start MongoDB service
3. Use default connection: `mongodb://localhost:27017`

---

### 3. Configure Environment

Edit the `.env` file:
```env
MONGODB_URL=your-mongodb-connection-string-here
DATABASE_NAME=search_engine_db
SECRET_KEY=your-secret-key-here
```

---

### 4. Start the Application

```bash
uvicorn main:app --reload
```

The API will start at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

---

## 🧪 Testing the API

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Test 2: Sign Up
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"username\":\"testuser\",\"password\":\"password123\"}"
```

### Test 3: Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

Save the `access_token` from the response!

### Test 4: Create Document
```bash
curl -X POST http://localhost:8000/api/documents \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d "{\"title\":\"Python Tutorial\",\"content\":\"Python is a high-level programming language\"}"
```

### Test 5: Search
```bash
curl "http://localhost:8000/api/search?q=python&page=1&limit=10"
```

---

## 🌐 Using the Interactive API Docs

1. Open http://localhost:8000/docs in your browser
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"
6. See the response!

**For protected endpoints:**
1. First, login to get a token
2. Click the "Authorize" button at the top
3. Enter: `Bearer YOUR_TOKEN_HERE`
4. Now you can access protected endpoints!

---

## 📊 Example Workflow

1. **Sign up** a new user
2. **Login** to get JWT token
3. **Create** several documents:
   - "Introduction to Python"
   - "JavaScript Basics"
   - "Python Data Science"
4. **Search** for "python"
5. **View results** ranked by relevance!

---

## 🚀 Deployment

When ready to deploy:
1. Set up MongoDB Atlas (if not already done)
2. Follow the `DEPLOYMENT.md` guide
3. Deploy to Render, Railway, or Heroku
4. Test the production API

---

## 🐛 Troubleshooting

### MongoDB Connection Error
- Check if MongoDB is running (local) or connection string is correct (Atlas)
- Verify network access in MongoDB Atlas
- Check `.env` file has correct MONGODB_URL

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.9+)

### Port Already in Use
- Change the port: `uvicorn main:app --reload --port 8001`

---

## 📚 Next Steps

- Read `ARCHITECTURE.md` to understand the system design
- Check `ROADMAP.md` for future enhancements
- Explore the code to learn about search algorithms
- Deploy to production!

---

## 🎯 Key Features

✅ User authentication with JWT  
✅ Document upload and management  
✅ Inverted index for fast search  
✅ TF-IDF ranking algorithm  
✅ RESTful API with auto-generated docs  
✅ MongoDB integration  
✅ Ready for deployment  

Happy searching! 🔍
