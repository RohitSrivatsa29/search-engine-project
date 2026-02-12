import asyncio
import httpx
import time

async def test_search():
    print("🚀 Testing Search API backend connectivity...")
    started = time.time()
    try:
        async with httpx.AsyncClient() as client:
            # 1. Root check (index.html)
            print("1. Pinging / (Root) endpoint...")
            resp = await client.get("http://localhost:8001/", timeout=5.0)
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                print("   ✅ Root page served!")
            else:
                print(f"   ❌ Root check failed: {resp.status_code}")

            # 2. Upload check (upload.html)
            print("\n2. Pinging /upload endpoint...")
            resp = await client.get("http://localhost:8001/upload", timeout=5.0)
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                print("   ✅ Upload page served!")
            
            # 3. Health check
            print("\n3. Pinging /health endpoint...")
            resp = await client.get("http://localhost:8001/health", timeout=5.0)
            print(f"   Status: {resp.status_code}")
            
            # 4. Search check
            print("\n4. Pinging /api/search?q=python...")
            resp = await client.get("http://localhost:8001/api/search?q=python", timeout=10.0)
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"   Results found: {data.get('total_results', 0)}")
                print(f"   First result: {data.get('results', [{}])[0].get('title', 'None')}")
            else:
                print(f"   Error: {resp.text}")

    except Exception as e:
        print(f"\n❌ Setup Check Failed: {e}")
        print("💡 Possible causes:")
        print("   - Server is not running")
        print("   - MongoDB connection timeout (check internet/password)")
        print("   - Firewall blocking port 8000")
    
    print(f"\n⏱️ Test took: {time.time() - started:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(test_search())
