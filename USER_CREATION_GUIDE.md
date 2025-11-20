# User Creation with Email Verification

## Overview
The `create_user()` function now automatically sends a verification email to new users when they are created.

## Usage

### Basic User Creation (With Verification Email)
```python
from fire_store_client import create_user

# Create user and send verification email automatically
user = create_user(
    email="newuser@example.com",
    password="SecurePassword123",
    display_name="John Doe"
)

if user:
    print(f"User created with UID: {user.uid}")
    print("Verification email sent!")
else:
    print("Failed to create user")
```

### Create User Without Verification Email
```python
from fire_store_client import create_user

# Create user but skip verification email
user = create_user(
    email="newuser@example.com",
    password="SecurePassword123",
    display_name="John Doe",
    send_verification=False  # Skip email
)
```

### Batch Create Users
```python
from fire_store_client import create_user

users_to_create = [
    {"email": "user1@example.com", "password": "Pass123", "display_name": "User One"},
    {"email": "user2@example.com", "password": "Pass456", "display_name": "User Two"},
    {"email": "user3@example.com", "password": "Pass789", "display_name": "User Three"},
]

for user_data in users_to_create:
    user = create_user(**user_data)
    if user:
        print(f"✓ Created and sent verification to {user_data['email']}")
    else:
        print(f"✗ Failed to create {user_data['email']}")
```

## What Happens

### 1. User Creation
- Firebase Authentication creates the user account
- User gets a unique UID
- Account is created but **not verified** initially

### 2. Verification Email Sent
- Beautiful HTML email sent automatically
- Contains "Verify Email" button
- Link expires in 1 hour
- User clicks button to verify their email

### 3. Email Template
The user receives an email with:
- **Subject**: "Verify Your Email - California Black Power Book"
- **Header**: Purple gradient with branding
- **Button**: Large "Verify Email" call-to-action
- **Alternative Link**: Copy-paste option
- **Security Info**: Link expiration notice

## Function Parameters

```python
def create_user(email, password, display_name=None, send_verification=True):
    """
    Args:
        email (str): User's email address (required)
        password (str): User's password (required)
        display_name (str): Optional display name
        send_verification (bool): Send verification email (default: True)

    Returns:
        User object if successful, None if failed
    """
```

## Error Handling

The function handles errors gracefully:
- **User creation fails**: Returns `None`, prints error
- **Email sending fails**: User is still created, but warning is printed
- **No .env configured**: User created, email fails silently

### Example Error Handling
```python
from fire_store_client import create_user

user = create_user("test@example.com", "password123")

if user:
    print(f"Success! User ID: {user.uid}")
    print(f"Email: {user.email}")
    print(f"Email Verified: {user.email_verified}")
else:
    print("Failed to create user - check console for errors")
```

## Console Output

### Successful Creation
```
User created successfully: abc123xyz - newuser@example.com
Email verification link generated: https://...
Message sent successfully to newuser@example.com
Verification email sent to newuser@example.com
```

### Email Failure (User Still Created)
```
User created successfully: abc123xyz - newuser@example.com
Error sending verification email: [error details]
```

## Integration Examples

### Create User From Web Form
```python
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    user = create_user(email, password, display_name=name)

    if user:
        return jsonify({
            "success": True,
            "message": "Account created! Check your email to verify.",
            "uid": user.uid
        }), 201
    else:
        return jsonify({
            "error": "Failed to create account"
        }), 500
```

### Create Admin User
```python
from fire_store_client import create_user, add_admin

# Create Firebase user with verification
user = create_user(
    email="admin@example.com",
    password="AdminPass123",
    display_name="Admin User"
)

if user:
    # Add to admins collection
    add_admin(
        email="admin@example.com",
        user_name="Admin User",
        phone="+1234567890",
        mfa_enabled=True
    )
    print("Admin user created and verification email sent!")
```

## User Verification Flow

1. **Admin creates user account**
   ```python
   create_user("user@example.com", "password")
   ```

2. **User receives email**
   - Email arrives in inbox
   - Contains verification link

3. **User clicks "Verify Email" button**
   - Redirected to Firebase auth page
   - Email marked as verified

4. **User can now login**
   - Goes to `/login` page
   - Uses email + password
   - Logged in successfully

## Testing

### Test User Creation Locally
```python
# test_user_creation.py
from fire_store_client import create_user

# Test with your email
test_user = create_user(
    email="your-email@gmail.com",
    password="TestPassword123",
    display_name="Test User"
)

if test_user:
    print("✓ User created!")
    print(f"  UID: {test_user.uid}")
    print(f"  Email: {test_user.email}")
    print(f"  Verified: {test_user.email_verified}")
    print("\n📧 Check your email for verification link!")
else:
    print("✗ Failed to create user")
```

Run:
```bash
python test_user_creation.py
```

## Troubleshooting

### Email Not Received?
1. ✓ Check spam/junk folder
2. ✓ Verify .env has `EMAIL_SENDER` and `EMAIL_PASS`
3. ✓ Check console output for errors
4. ✓ Verify Gmail App Password is valid

### User Created But Not Verified?
- This is normal! User must click the link in email
- Check `user.email_verified` - should be `False` initially
- After clicking email link, it becomes `True`

### Can't Send Verification Email?
```python
# Send manually later
from firebase_auth_client import send_auth_link

send_auth_link("user@example.com")
```

## Best Practices

1. ✅ **Always send verification** for new users
2. ✅ **Use strong passwords** when creating accounts
3. ✅ **Handle errors gracefully** in production
4. ✅ **Log user creation** for audit trail
5. ✅ **Test email delivery** before deploying
6. ✅ **Provide feedback** to users about verification

## Security Notes

- Verification links expire after **1 hour**
- Users can't login until verified (optional to enforce)
- Passwords are securely hashed by Firebase
- Email verification prevents fake accounts
- Use HTTPS for all authentication flows
