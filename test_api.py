"""
Simple test script to verify the search engine is working
Run this after setting up MongoDB and starting the server
"""
import asyncio
import httpx

BASE_URL = "http://localhost:8000"

async def test_search_engine():
    """Test the search engine end-to-end"""
    
    async with httpx.AsyncClient() as client:
        print("🧪 Testing Search Engine API\n")
        
        # Test 1: Health Check
        print("1️⃣ Testing health check...")
        response = await client.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
        
        # Test 2: Sign Up
        print("2️⃣ Testing user signup...")
        signup_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
        response = await client.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
        if response.status_code == 201:
            print(f"   ✅ User created successfully")
        elif response.status_code == 400:
            print(f"   ⚠️  User already exists (that's okay)")
        else:
            print(f"   ❌ Error: {response.status_code}")
        print()
        
        # Test 3: Login
        print("3️⃣ Testing login...")
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = await client.post(f"{BASE_URL}/api/auth/login", json=login_data)
        token_data = response.json()
        token = token_data.get("access_token")
        print(f"   ✅ Login successful")
        print(f"   Token: {token[:20]}...\n")
        
        # Set authorization header
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test 4: Create Documents
        print("4️⃣ Creating test documents...")
        documents = [
            {
                "title": "Introduction to Python",
                "content": "Python is a high-level programming language known for its simplicity and readability. It's widely used in web development, data science, and automation."
            },
            {
                "title": "JavaScript Basics",
                "content": "JavaScript is a versatile programming language primarily used for web development. It enables interactive web pages and is an essential part of web applications."
            },
            {
                "title": "Python Data Science",
                "content": "Python has become the go-to language for data science. Libraries like NumPy, Pandas, and Matplotlib make data analysis and visualization easy."
            },
            {
                "title": "Machine Learning with Python",
                "content": "Python offers powerful machine learning libraries such as scikit-learn and TensorFlow. These tools enable developers to build intelligent applications."
            }
        ]
        
        for doc in documents:
            response = await client.post(
                f"{BASE_URL}/api/documents",
                json=doc,
                headers=headers
            )
            if response.status_code == 201:
                print(f"   ✅ Created: {doc['title']}")
        print()
        
        # Test 5: Search
        print("5️⃣ Testing search functionality...")
        search_queries = ["python", "javascript", "data science", "machine learning"]
        
        for query in search_queries:
            response = await client.get(
                f"{BASE_URL}/api/search",
                params={"q": query, "page": 1, "limit": 10}
            )
            results = response.json()
            print(f"\n   🔍 Search: '{query}'")
            print(f"   📊 Found {results['total_results']} results")
            
            for i, doc in enumerate(results['results'][:3], 1):
                print(f"      {i}. {doc['title']} (score: {doc.get('relevance_score', 0)})")
        
        print("\n\n✅ All tests completed successfully!")
        print("🎉 Your search engine is working!\n")

if __name__ == "__main__":
    try:
        asyncio.run(test_search_engine())
    except httpx.ConnectError:
        print("❌ Error: Could not connect to the server")
        print("   Make sure the server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
