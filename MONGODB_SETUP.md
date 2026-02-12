# MongoDB Setup Guide

## Option 1: MongoDB Atlas (Recommended - Cloud, Free)

### Step 1: Create Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a free account
3. Choose the **FREE** tier (M0 Sandbox)

### Step 2: Create Cluster
1. After signup, click "Build a Database"
2. Choose **FREE** shared cluster
3. Select a cloud provider and region (choose closest to you)
4. Click "Create Cluster"

### Step 3: Create Database User
1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Set username and password (save these!)
5. Set privileges to "Read and write to any database"
6. Click "Add User"

### Step 4: Allow Network Access
1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (for development)
4. Click "Confirm"

### Step 5: Get Connection String
1. Go to "Database" in the left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string
5. It looks like: `mongodb+srv://username:<password>@cluster.mongodb.net/`

### Step 6: Update .env File
Replace the `MONGODB_URL` in your `.env` file:
```
MONGODB_URL=mongodb+srv://your-username:your-password@cluster.mongodb.net/search_engine_db?retryWrites=true&w=majority
```

**Important**: Replace `your-username` and `your-password` with your actual credentials!

---

## Option 2: Local MongoDB (Advanced)

### Windows Installation
1. Download MongoDB Community Server from [mongodb.com/download-center/community](https://www.mongodb.com/try/download/community)
2. Run the installer
3. Choose "Complete" installation
4. Install as a Windows Service
5. MongoDB will run on `mongodb://localhost:27017`

### Start MongoDB Service
```powershell
net start MongoDB
```

### Verify MongoDB is Running
```powershell
mongosh
```

---

## Testing the Connection

After setting up MongoDB (Atlas or Local), test the connection:

```bash
cd f:\search-engine-project
python -c "import asyncio; from mongodb import connect_db; asyncio.run(connect_db())"
```

You should see: `✅ Connected to MongoDB: search_engine_db`

---

## Next Steps

Once MongoDB is connected, you can:
1. Start the application: `uvicorn main:app --reload`
2. Access API docs: http://localhost:8000/docs
3. Test the endpoints!
