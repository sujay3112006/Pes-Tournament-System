# Authentication Fix - Quick Testing Guide

## 🚀 How to Verify the Fixes

### Test 1: Login Flow
```bash
# 1. Start backend
cd Backend
python manage.py runserver

# 2. Start frontend
cd Frontend
npm run dev

# 3. Open http://localhost:5173 and login
# Expected: Login → Dashboard shows (no immediate redirect)
```

**Console Output Expected:**
```
✅ access_token: eyJ...
✅ user: {user data}
💾 handleLogin called
💾 Tokens saved
✅ ProtectedRoute: Allowing access
🛡️ ProtectedRoute rendering: {isAuthenticated: true, hasToken: true}
📚 Dashboard: Loading data...
✅ Dashboard: Profile loaded
```

---

### Test 2: Token Validation
```javascript
// In browser console after login:

// Check 1: Token exists
localStorage.getItem('access_token')
// Output: Should show 32+ character token

// Check 2: Token in requests
// Open Network tab → Click profile request → Headers
// Should see: Authorization: Bearer {token}

// Check 3: Backend validates it
// Backend console should show: ✅ Authentication successful
```

---

### Test 3: Error Handling
```javascript
// Simulate 401 error - paste in console after login:
localStorage.setItem('access_token', 'invalid_token_test')
// Refresh dashboard
// Expected: Error message "Your session has expired"
// Then: Stays on error for 2 seconds before redirecting
```

---

### Test 4: Network Inspection

**Good Request Sequence:**
```
POST /auth/login/
Response: 200
Body: {access, refresh, user}
↓
GET /auth/profile/ 
Headers: Authorization: Bearer {token}
Response: 200
Body: {username, coins, stats...}
↓
Status: ✅ Logged in and dashboard loads
```

**Bad Request Sequence (OLD - don't do this):**
```
POST /auth/login/
Response: 200
Body: {access, refresh, user}
↓
localStorage cleared (by 401 interceptor)
↓
GET /auth/profile/
Headers: (no Authorization)
Response: 401
↓
Redirect to /login immediately
Status: ❌ Infinite loop
```

---

## 🔧 Key Files Modified

### Backend
1. **`core/settings.py`**
   - Changed `DEFAULT_AUTHENTICATION_CLASSES` to include `SimpleTokenAuthentication`
   - Changed `DEFAULT_PERMISSION_CLASSES` to `IsAuthenticatedOrReadOnly`

2. **`core/authentication.py`**
   - Added `_token_store` dictionary
   - Added `generate_token()` function
   - Added `validate_token()` function
   - Enhanced `SimpleTokenAuthentication` class

3. **`apps/users/views.py`**
   - Updated `RegisterView` to use `generate_token()`
   - Updated `LoginView` to use `generate_token()`
   - Fixed `LogoutView` to not require RefreshToken

### Frontend
1. **`src/services/api.js`**
   - Enhanced request interceptor with logging
   - Improved 401 response handler
   - Added token refresh attempt
   - Added delay before redirect

2. **`src/pages/DashboardPage.jsx`**
   - Added error state
   - Added try-catch for each API call
   - Separate load for tournaments/matches
   - User-friendly error messages
   - Delayed navigation on error

3. **`src/App.jsx`**
   - Enhanced logging in ProtectedRoute

---

## 📊 Before vs After

| Scenario | Before | After |
|----------|--------|-------|
| Login → Dashboard | ✗ Instant redirect to login | ✅ Dashboard loads and stays |
| Token verification | ❌ Not validated | ✅ Backend validates each request |
| 401 error | ❌ Hard redirect | ✅ 500ms delay + error display |
| Profile load fail | ❌ Silent failure | ✅ User-friendly error message |
| API logs | ❌ None | ✅ Console + backend logs |

---

## 🧠 How It Works Now

### Login Process:
```
User enters credentials
    ↓
Frontend: POST /auth/login/ {username, password}
    ↓
Backend: Validates → Creates token → Stores in _token_store
    ↓
Response: {user, access: token, refresh: token}
    ↓
Frontend: Saves to localStorage
    ↓
Frontend: Navigates to Dashboard
```

### Dashboard Load:
```
Dashboard component mounts
    ↓
useEffect calls: authService.getProfile()
    ↓
Axios interceptor: Adds Authorization header with token
    ↓
Backend receives request with token
    ↓
SimpleTokenAuthentication: Validates token from _token_store
    ↓
Returns authenticated user object
    ↓
ProfileView: Sees IsAuthenticated = True
    ↓
Returns profile data
    ↓
Dashboard: Displays stats and stays on page
```

---

## ⚠️ Common Issues & Fixes

### Issue: Still getting infinite loop
```javascript
// Check 1: Clear everything
localStorage.clear()
sessionStorage.clear()

// Check 2: Verify token endpoint working
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'

// Check 3: Verify profile endpoint
curl -X GET http://localhost:8000/api/v1/auth/profile/ \
  -H "Authorization: Bearer {token_from_login}"
// Should return 200 with user data, not 401
```

### Issue: 401 even with token
```javascript
// Check backend token store
// In Backend Python shell:
from core.authentication import _token_store
print(_token_store)
# Should show: {'token_string': 'user_id'}

# If empty, token wasn't generated correctly
# If token not in dict, backend auth not working
```

### Issue: Token disappears
```javascript
// Trace where it's being removed
// Add this to localStorage before login:
const originalSetItem = localStorage.setItem
const originalRemoveItem = localStorage.removeItem

localStorage.setItem = function(key, value) {
  if (key === 'access_token') console.trace('access_token SET', value)
  return originalSetItem(key, value)
}

localStorage.removeItem = function(key) {
  if (key === 'access_token') console.trace('access_token REMOVED')
  return originalRemoveItem(key)
}

// Now login and watch console
// You'll see exact line that removes token
```

---

## ✅ Verification Checklist

After implementing fixes, verify:

- [ ] Backend running: `python manage.py runserver`
- [ ] Frontend running: `npm run dev`
- [ ] Login works without error
- [ ] Dashboard loads after login
- [ ] Console shows ✅ messages (not ❌)
- [ ] No 401 status in Network tab
- [ ] Token in localStorage persists
- [ ] Refresh page → stays logged in
- [ ] Logout clears token
- [ ] Can login again after logout

---

## 🎯 Expected Console Logs

### Successful Login Flow:
```
🔄 Sending login request...
✅ Login response received: {access, refresh, user}
💾 handleLogin called
💾 Tokens saved
✅ ProtectedRoute: Allowing access
🛡️ ProtectedRoute rendering: {isAuthenticated: true}
📚 Dashboard: Loading data...
📤 Request sent with token: abc1234...
✅ API Response successful: 200
✅ Dashboard: Profile loaded: {username: "player1", coins: 500...}
```

### Dashboard Loads Complete:
```
✅ Dashboard: Tournaments loaded: 3
✅ Dashboard: Matches loaded: 2
```

### If Error Occurs:
```
❌ Dashboard: Error loading data: Error: Request failed with status code 401
⚠️ Your session has expired. Please log in again.
[2 second delay]
[Redirects to /login]
```

---

## 🔐 Token Lifecycle

```
1. CREATE: generate_token(user_id) → creates 32-char token
2. STORE: _token_store[token] = user_id
3. SEND: Frontend receives and stores in localStorage
4. USE: Include in Authorization header: "Bearer {token}"
5. VALIDATE: Backend looks up token in _token_store
6. AUTHENTICATE: Returns actual User object
7. AUTHORIZE: View checks IsAuthenticated permission
8. RESPOND: Returns data or 401 if invalid

All steps must work for authentication to succeed!
```

---

## 📞 Debugging Commands

```bash
# Backend - check token store
python manage.py shell
>>> from core.authentication import _token_store
>>> print(_token_store)

# Backend - test login manually
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

# Backend - check if profile works
TOKEN="your_token_here"
curl -X GET http://localhost:8000/api/v1/auth/profile/ \
  -H "Authorization: Bearer $TOKEN"

# Frontend - check localStorage
localStorage.getItem('access_token')
localStorage.getItem('refresh_token')
localStorage.getItem('user')

# Frontend - check network requests
# Open DevTools → Network → Login and watch requests
```

