import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 60)
print("🧪 TESTING FIXED TOURNAMENT ENDPOINT")
print("=" * 60)

# Step 1: Login
print("\n[STEP 1] Logging in...")
login_response = requests.post(
    f"{BASE_URL}/auth/login/",
    json={"username": "testuser", "password": "Test123456"},
    headers={"Content-Type": "application/json"}
)

if login_response.status_code == 200:
    token = login_response.json().get('access')
    user_id = login_response.json().get('user', {}).get('user_id')
    print(f"✅ Login successful")
    print(f"   Token: {token[:20]}...")
    print(f"   User ID: {user_id}")
else:
    print(f"❌ Login failed: {login_response.status_code}")
    exit(1)

# Step 2: Test GET /tournaments/ (list endpoint)
print("\n[STEP 2] Testing GET /tournaments/...")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
get_response = requests.get(f"{BASE_URL}/tournaments/", headers=headers)
print(f"Status: {get_response.status_code}")
if get_response.status_code == 200:
    print(f"✅ GET /tournaments/ working")
    print(f"   Response: {get_response.json()}")
else:
    print(f"❌ GET failed")
    print(f"   Response: {get_response.text}")

# Step 3: Test POST /tournaments/ (create endpoint)
print("\n[STEP 3] Testing POST /tournaments/...")
tournament_data = {
    "name": "Test Tournament",
    "description": "This is a test tournament",
    "max_players": 8,
    "status": "active",
    "prize_pool": 1000
}

post_response = requests.post(
    f"{BASE_URL}/tournaments/",
    json=tournament_data,
    headers=headers
)

print(f"Status: {post_response.status_code}")
if post_response.status_code in [200, 201]:
    print(f"✅ POST /tournaments/ working")
    print(f"   Response: {json.dumps(post_response.json(), indent=2)}")
else:
    print(f"❌ POST failed")
    print(f"   Response: {post_response.text}")

print("\n" + "=" * 60)
print("Testing Complete!")
print("=" * 60)
