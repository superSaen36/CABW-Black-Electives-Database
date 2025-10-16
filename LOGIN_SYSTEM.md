# Login System Documentation

## Overview
The login system now fully integrates with the admin feature, automatically detecting admin status during login and providing appropriate access levels.

## How It Works

### 1. Login Flow

#### Frontend (login.html)
1. User enters email and password
2. Firebase Authentication validates credentials
3. Firebase returns an ID token
4. Frontend sends ID token to backend `/login` endpoint
5. Backend validates token and checks admin status
6. User is redirected to home page with session established

#### Backend (app.py:371-403)
```python
@app.route("/login", methods=["GET", "POST"])
def login():
    # Verify Firebase ID token
    decoded_token = verify_id_token(id_token)

    # Check if user is admin
    user_email = decoded_token.get('email')
    user_is_admin = is_admin(user_email)  # Checks 'admins' collection

    # Create session with admin flag
    session['user'] = {
        'uid': decoded_token['uid'],
        'email': user_email,
        'name': decoded_token.get('name'),
        'is_admin': user_is_admin  # This is the key flag
    }

    return jsonify({"success": True, "is_admin": user_is_admin})
```

### 2. User Types

#### Regular Users
- **Can access**:
  - Home page (`/`)
  - Location search (`/location`)
  - News page with approved articles (`/news`)
  - Profile pages (`/profile/<id>`)
  - Wiki pages (`/wiki/<id>`)
  - Update officials (if logged in with `@login_required`)

- **Cannot access**:
  - Admin news controls (approve/disapprove buttons)
  - Article approval endpoints

#### Admin Users
- **Can access everything regular users can, PLUS**:
  - See ALL articles (approved and pending) on `/news`
  - Approve/disapprove buttons on news cards
  - Article approval endpoint (`/article/approve/<id>`)
  - Article disapproval endpoint (`/article/disapprove/<id>`)

### 3. Admin Detection

The system checks if a user is an admin by:
1. Looking up their email in the `admins` Firestore collection
2. Using the `is_admin(email)` function from `fire_store_client.py`
3. Setting `is_admin=True` in the session if found

```python
# From fire_store_client.py
def is_admin(email):
    """Check if a user is an admin"""
    admin = get_admin_by_email(email)
    return admin is not None
```

### 4. Access Control

#### Login Required Decorator
```python
@login_required
def some_route():
    # User must be logged in (regular or admin)
    pass
```

#### Admin Required Decorator
```python
@admin_required
def some_route():
    # User must be logged in AND be an admin
    pass
```

### 5. Session Management

After successful login, the session contains:
```python
session['user'] = {
    'uid': 'firebase-user-id',
    'email': 'user@example.com',
    'name': 'User Name',
    'is_admin': True/False  # Checked on every admin-protected route
}
```

## Setting Up Admins

### Adding Your First Admin
```bash
python admin_utils.py add your-email@example.com "Your Name" --phone "+1234567890"
```

### Checking Admin Status
```bash
python admin_utils.py check your-email@example.com
```

### Listing All Admins
```bash
python admin_utils.py list
```

## Testing the System

### Test Regular User Login
1. Create a Firebase user (not in admins collection)
2. Login at `/login`
3. Visit `/news` - should only see approved articles
4. No admin controls visible

### Test Admin Login
1. Add user to admins collection using `admin_utils.py`
2. Login at `/login`
3. Visit `/news` - should see all articles
4. Green/red approve/disapprove buttons visible
5. Can click buttons to approve/disapprove articles

## Security Features

### 1. Firebase Authentication
- All users must authenticate through Firebase
- ID tokens are verified server-side
- Tokens expire and must be refreshed

### 2. Server-Side Admin Checks
- Admin status is checked server-side, not client-side
- Cannot be bypassed by modifying frontend code
- Session flag is set during login, not by client

### 3. Route Protection
- Admin routes use `@admin_required` decorator
- Automatically redirect to login if not authenticated
- Return 403 error if authenticated but not admin

### 4. Session Security
- Secret key for session encryption
- Session stored server-side
- Admin status cannot be manipulated by client

## Common Issues & Solutions

### Issue: User is admin but doesn't see admin controls
**Solution**:
1. Check if email in `admins` collection matches exactly
2. Log out and log back in to refresh session
3. Check browser console for errors

### Issue: Login fails for existing Firebase user
**Solution**:
1. Verify Firebase configuration in `login.html`
2. Check if user exists in Firebase Authentication
3. Check backend logs for token verification errors

### Issue: Admin can't approve/disapprove articles
**Solution**:
1. Check if session has `is_admin=True`
2. Verify admin is still in `admins` collection
3. Check browser console for AJAX errors
4. Check Flask logs for endpoint errors

## Current Workflow

1. **User visits site** → Can see home, location, approved news
2. **User clicks Login** → Goes to `/login` page
3. **User enters credentials** → Firebase validates
4. **Backend checks admin status** → Queries `admins` collection
5. **Session created with admin flag** → User redirected to home
6. **Admin visits /news** → Sees all articles with controls
7. **Admin clicks approve/disapprove** → AJAX call to backend
8. **Backend verifies admin** → Updates article status
9. **Page reloads** → Shows updated article status

## Integration Points

### With Firebase
- Uses Firebase Authentication for user management
- Firestore for admin data storage
- ID tokens for secure authentication

### With Flask
- Session management for user state
- Decorators for route protection
- JSON API for article approval

### With Frontend
- AJAX calls for approve/disapprove
- Dynamic button states based on admin status
- Visual indicators for article status

## Future Enhancements

1. **Role-Based Access Control**: Add multiple admin roles (super admin, editor, moderator)
2. **Activity Logging**: Track who approved/disapproved which articles
3. **Admin Dashboard**: Dedicated page showing admin statistics
4. **Email Notifications**: Send emails when new articles need approval
5. **MFA Implementation**: Add multi-factor authentication for admins
