# Quick Start: Email Authentication

## Setup (One-Time)

### 1. Configure Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Enable **2-Factor Authentication** (Security → 2-Step Verification)
3. Generate an **App Password**:
   - Go to Security → 2-Step Verification → App passwords
   - Select "Mail" and "Other (Custom name)"
   - Name it "CABW App"
   - Copy the 16-character password

### 2. Create/Update .env File

Create a `.env` file in the project root:

```bash
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASS=your-16-char-app-password
SECRET_KEY=your-secret-key-here
```

## Testing

### Test Password Reset Email

```bash
python -c "from firebase_auth_client import send_password_reset_email; send_password_reset_email('your-email@gmail.com')"
```

### Test Sign-In Email

```bash
python -c "from firebase_auth_client import send_email_login; send_email_login('your-email@gmail.com')"
```

## Usage in App

### 1. Password Reset (Already Integrated)

**On Login Page:**
1. Enter your email
2. Click "Forgot password?"
3. Check your email for reset link
4. Click the button in the email
5. Reset your password

### 2. Send Test Email via Python

```python
from firebase_auth_client import send_password_reset_email

# Send password reset
send_password_reset_email("user@example.com")
```

### 3. Send to Multiple Users

```python
from firebase_auth_client import send_password_reset_email
from fire_store_client import get_collection_data

# Send to all admins
admins = get_collection_data("admins")
for admin in admins:
    email = admin.to_dict()['email']
    send_password_reset_email(email)
```

## Troubleshooting

### Email Not Sending?

1. **Check .env file exists** and has correct values
2. **Verify App Password** (16 chars, no spaces)
3. **Enable 2FA** on Gmail account
4. **Check spam folder**
5. **Look at console output** for error messages

### Link Not Working?

1. **Check Firebase console** - Email/Password auth enabled?
2. **Verify redirect URL** matches your Firebase config
3. **Links expire after 1 hour** - request a new one

## Email Features

✅ **Professional HTML Templates** - Styled emails with buttons
✅ **Three Email Types** - Verification, Sign-in, Password Reset
✅ **Alternative Links** - Copy-paste option if buttons don't work
✅ **Security Info** - Shows link expiration time
✅ **Branded Design** - Matches your app's purple gradient theme

## API Endpoints

### POST /forgot-password
Send password reset email

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Password reset link sent to your email"
}
```

### POST /request-login-link
Send passwordless login link

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Sign-in link sent to your email"
}
```

## Next Steps

1. ✅ Set up Gmail App Password
2. ✅ Configure .env file
3. ✅ Test with your email
4. ✅ Try forgot password on login page
5. 🔄 Integrate with user registration (optional)
6. 🔄 Add email notifications for admins (optional)
