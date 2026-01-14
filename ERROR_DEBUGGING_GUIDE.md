# HTTP Error Debugging Guide

## Common HTTP Errors & Solutions

### 🔴 HTTP 405 - Method Not Allowed

**What it means:**
The server recognized your request but the HTTP method (GET, POST, PATCH, DELETE, PUT) is not allowed for that specific endpoint.

**Example from your case:**
```
Request:  PATCH http://localhost:8000/api/tasks/15
Response: 405 Method Not Allowed
```

**Why it happened:**
```
Backend defined:        ❌ PATCH /api/tasks/{id}  (not defined)
What I called instead:  ✅ PATCH /api/tasks/{id}/complete  (exists)
```

**Solution:**
```javascript
// WRONG - endpoint doesn't support PATCH
fetch('/api/tasks/15', { method: 'PATCH' })

// CORRECT - use the right endpoint
fetch('/api/tasks/15/complete', { method: 'PATCH' })
```

**Debugging:**
1. Check backend routes documentation
2. Verify the endpoint exists in your API
3. Ensure HTTP method matches the backend (GET, POST, PUT, PATCH, DELETE)

---

### 🔴 HTTP 401 - Unauthorized

**What it means:**
The server requires authentication and either:
- No token was provided
- Token is invalid/expired
- Token format is wrong

**Common causes:**
```javascript
// ❌ No token
fetch('/api/tasks', {
  headers: { 'Content-Type': 'application/json' }
})

// ✅ With token
fetch('/api/tasks', {
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGc...'  // ← Token here
  }
})
```

**Debug checklist:**
```javascript
// 1. Check if token exists
const token = localStorage.getItem('access_token');
console.log('Token exists:', !!token);

// 2. Check token format (should start with 'eyJ')
console.log('Token prefix:', token?.substring(0, 10));

// 3. Verify it's a valid JWT (3 parts separated by dots)
const parts = token?.split('.');
console.log('Valid JWT format:', parts?.length === 3);

// 4. Check if token might be expired
const payload = JSON.parse(atob(parts[1])); // Decode middle part
const expiresAt = new Date(payload.exp * 1000);
console.log('Token expires at:', expiresAt);
console.log('Token expired:', expiresAt < new Date());
```

**Solution:**
1. Ensure token is included in Authorization header
2. Format: `Authorization: Bearer <token>` (note the space)
3. Check if token has expired - re-login if needed

---

### 🟡 HTTP 404 - Not Found

**What it means:**
The server doesn't have the resource you're asking for.

**Examples:**
```
GET /api/tasks/999  → 404 (task doesn't exist)
GET /api/users/abc  → 404 (endpoint doesn't exist)
```

**Solution:**
1. Check the resource ID exists
2. Verify the endpoint path is correct
3. Make sure it's the right API version (/api/v1 vs /api)

---

### 🟠 HTTP 500 - Internal Server Error

**What it means:**
An unexpected error occurred on the server.

**How to debug:**
1. Check backend logs/console
2. Look for stack traces
3. Verify database connection
4. Check environment variables

---

## API Testing Tools

### 1. Using Browser DevTools

```javascript
// Open Console and test:
const token = localStorage.getItem('access_token');

// Test endpoint
fetch('http://localhost:8000/api/tasks', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(res => res.json())
.then(data => console.log('Response:', data))
.catch(err => console.error('Error:', err));
```

### 2. Using cURL

```bash
# Set your token
TOKEN="your_token_here"

# Test GET endpoint
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/tasks

# Test PATCH endpoint
curl -X PATCH \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8000/api/tasks/15/complete

# Test POST endpoint
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"Test task"}' \
  http://localhost:8000/api/tasks
```

### 3. Using Postman

1. Create a new request
2. Set method (GET, POST, PATCH, etc.)
3. Enter URL
4. Add header: `Authorization: Bearer <token>`
5. Add body (if needed)
6. Send and check response

---

## Request/Response Debugging

### Checking Request Details

```javascript
// In browser DevTools → Network tab:

// Look for your API request
// Click on it and check:
1. Headers tab → verify Authorization header
2. Payload tab → verify JSON body
3. Response tab → see what server returned
4. Status → HTTP status code
```

### Common Header Issues

```javascript
// ❌ WRONG - Missing "Bearer"
Authorization: <token>

// ✅ CORRECT - Include "Bearer" prefix
Authorization: Bearer <token>

// ❌ WRONG - Missing Content-Type
headers: { 'Authorization': 'Bearer ...' }

// ✅ CORRECT - Include Content-Type
headers: {
  'Authorization': 'Bearer ...',
  'Content-Type': 'application/json'
}
```

---

## API Endpoint Checklist

Before making any API call:

- [ ] **Method Correct?** (GET, POST, PATCH, PUT, DELETE)
- [ ] **URL Correct?** (exact path, correct ID)
- [ ] **Token Present?** (in localStorage and headers)
- [ ] **Token Valid?** (not expired, correct format)
- [ ] **Headers Correct?** (Authorization: Bearer token, Content-Type)
- [ ] **Body Valid?** (if POST/PUT/PATCH, check JSON format)
- [ ] **CORS Allowed?** (frontend URL allowed by backend)

---

## Your Specific Error - Root Cause Analysis

### The Problem

**Frontend Code:**
```typescript
// Line 124-142 in tasks/page.tsx
fetch(`/api/tasks/${taskId}`, {  // ← Wrong endpoint!
  method: 'PATCH',
  headers: { 'Authorization': `Bearer ${token}` },
  body: JSON.stringify({ completed: true })
})
```

**Backend Routes:**
```python
# tasks.py - Only these routes exist:
GET    /api/tasks           ✅
POST   /api/tasks           ✅
GET    /api/tasks/{id}      ✅
PUT    /api/tasks/{id}      ✅
DELETE /api/tasks/{id}      ✅
PATCH  /api/tasks/{id}/complete  ← This is what we need!
```

**Error:**
```
Request:  PATCH /api/tasks/15  ❌ Not supported
Backend:  No PATCH handler for /api/tasks/{id}
Response: 405 Method Not Allowed
```

### The Solution

```typescript
// FIXED - Use correct endpoint
fetch(`/api/tasks/${taskId}/complete`, {  // ← Correct endpoint
  method: 'PATCH',
  headers: { 'Authorization': `Bearer ${token}` }
  // No body needed - backend toggles automatically
})
```

---

## Best Practices

### 1. Always Test Before Production

```bash
# Test your API endpoint with curl
curl -X PATCH \
  -H "Authorization: Bearer $YOUR_TOKEN" \
  http://localhost:8000/api/tasks/1/complete
```

### 2. Check API Documentation

Before implementing, always:
- [ ] Check endpoint URL
- [ ] Check HTTP method
- [ ] Check required headers
- [ ] Check request body format
- [ ] Check response format

### 3. Handle Errors Gracefully

```typescript
try {
  const response = await fetch(url, options);
  
  if (response.status === 401) {
    // Token expired - redirect to login
    redirectToLogin();
  } else if (response.status === 404) {
    // Resource not found
    showError('Item not found');
  } else if (response.status === 405) {
    // Wrong HTTP method
    console.error('API endpoint mismatch');
  } else if (!response.ok) {
    // Other errors
    throw new Error(`HTTP ${response.status}`);
  }
  
  return await response.json();
} catch (err) {
  console.error('Request failed:', err);
  showError('Something went wrong');
}
```

### 4. Log for Debugging

```typescript
// Always log requests in development
console.log('Request:', { method, url, headers });
console.log('Response status:', response.status);
console.log('Response body:', await response.json());
```

---

## Quick Reference

| Code | Meaning | Action |
|------|---------|--------|
| 200 | OK | Success ✅ |
| 201 | Created | Resource created ✅ |
| 204 | No Content | Success, no data |
| 400 | Bad Request | Check request format |
| 401 | Unauthorized | Check token |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Check endpoint URL |
| 405 | Not Allowed | Check HTTP method |
| 500 | Server Error | Check backend logs |

---

**Remember:** When debugging API errors:
1. Check the status code
2. Read the error message
3. Verify request format
4. Check token validity
5. Test with curl first
6. Review backend logs

Happy debugging! 🚀
