import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 60)
print("🧪 AUTHENTICATION TEST")
print("=" * 60)

# Test 1: Login
print("\n[TEST 1] Testing Login...")
login_data = {
    "username": "testuser",
    "password": "Test123456"
}

try:
    response = requests.post(
        f"{BASE_URL}/auth/login/",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Login successful!")
        print(f"Response: {json.dumps(data, indent=2)}")
        
        # Extract token
        token = data.get('access')
        if token:
            print(f"\n✅ Token generated: {token[:20]}...")
            
            # Test 2: Use token for protected endpoint
            print("\n[TEST 2] Testing Protected Endpoint with Token...")
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            profile_response = requests.get(
                f"{BASE_URL}/auth/profile/",
                headers=headers
            )
            
            print(f"Status: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                print("✅ Protected endpoint accessible!")
                profile_data = profile_response.json()
                print(f"Response: {json.dumps(profile_data, indent=2)}")
            else:
                print(f"❌ Protected endpoint failed")
                print(f"Response: {profile_response.text}")
        else:
            print("❌ No token in response")
    else:
        print(f"❌ Login failed with status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("Testing Complete!")
print("=" * 60)
