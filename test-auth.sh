#!/bin/bash
# Authentication Testing Script

echo "🧪 AUTHENTICATION FIX VERIFICATION"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Backend is running
echo -e "${YELLOW}[TEST 1]${NC} Checking if backend is running..."
if curl -s http://localhost:8000/api/v1/auth/login/ > /dev/null; then
    echo -e "${GREEN}✅${NC} Backend is responding"
else
    echo -e "${RED}❌${NC} Backend is not responding. Make sure Django is running."
    exit 1
fi

# Test 2: Login endpoint exists
echo ""
echo -e "${YELLOW}[TEST 2]${NC} Testing login endpoint..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test123456"}')

if echo "$RESPONSE" | grep -q "access"; then
    echo -e "${GREEN}✅${NC} Login endpoint working"
    echo "Response: $RESPONSE"
else
    echo -e "${RED}❌${NC} Login endpoint failed"
    echo "Response: $RESPONSE"
fi

# Test 3: Token validation
echo ""
echo -e "${YELLOW}[TEST 3]${NC} Checking token generation..."
TOKEN=$(echo "$RESPONSE" | grep -o '"access":"[^"]*' | cut -d'"' -f4)
if [ ! -z "$TOKEN" ]; then
    echo -e "${GREEN}✅${NC} Token generated: ${TOKEN:0:20}..."
else
    echo -e "${RED}❌${NC} No token in response"
fi

# Test 4: Profile endpoint with token
echo ""
echo -e "${YELLOW}[TEST 4]${NC} Testing protected endpoint with token..."
if [ ! -z "$TOKEN" ]; then
    PROFILE=$(curl -s -X GET http://localhost:8000/api/v1/auth/profile/ \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json")
    
    if echo "$PROFILE" | grep -q "username"; then
        echo -e "${GREEN}✅${NC} Protected endpoint working"
        echo "Profile: $PROFILE"
    else
        echo -e "${RED}❌${NC} Protected endpoint failed"
        echo "Response: $PROFILE"
    fi
else
    echo -e "${YELLOW}⚠️${NC}  Skipping (no token)"
fi

echo ""
echo "===================================="
echo -e "${GREEN}Testing Complete!${NC}"
