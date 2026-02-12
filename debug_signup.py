"""
Simpler test to debug the signup issue
"""
import asyncio
import httpx
import json

async def test_signup():
    async with httpx.AsyncClient() as client:
        print("Testing signup endpoint...")
        
        signup_data = {
            "email": "debug@example.com",
            "username": "debuguser",
            "password": "testpass123"
        }
        
        try:
            response = await client.post(
                "http://localhost:8000/api/auth/signup",
                json=signup_data,
                timeout=10.0
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 201:
                print("✅ Signup successful!")
            else:
                print(f"❌ Signup failed")
                try:
                    error_detail = response.json()
                    print(f"Error details: {json.dumps(error_detail, indent=2)}")
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_signup())
