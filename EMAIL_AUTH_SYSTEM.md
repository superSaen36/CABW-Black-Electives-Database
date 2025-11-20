# Email Authentication System

## Overview
The firebase_auth_client.py now sends beautifully formatted HTML emails with verification links to users for authentication purposes.

## Features

### 1. **Email Verification Links**
Send email verification links to newly registered users.

```python
from firebase_auth_client import send_auth_link

# Send verification email
link = send_auth_link("user@example.com")
```

### 2. **Passwordless Sign-In Links**
Send magic links for passwordless authentication.

```python
from firebase_auth_client import send_email_login

# Send sign-in link
link = send_email_login("user@example.com")
```

### 3. **Password Reset Links**
Send password reset emails.

```python
from firebase_auth_client import send_password_reset_email

# Send password reset email
link = send_password_reset_email("user@example.com")
```

## Email Templates

All emails use professional HTML templates with:
- **Branded Header** - Purple gradient with "California Black Power Book" title
- **Styled Button** - Large, prominent call-to-action button
- **Alternative Link** - Copy-paste option for email clients that don't support buttons
- **Footer** - Security information and branding

### Email Types

#### 1. Verification Email
- **Subject**: "Verify Your Email - California Black Power Book"
- **Button**: "Verify Email"
- **Use Case**: New user registration

#### 2. Sign-In Email
- **Subject**: "Sign In to California Black Power Book"
- **Button**: "Sign In"
- **Use Case**: Passwordless authentication

#### 3. Password Reset Email
- **Subject**: "Reset Your Password - California Black Power Book"
- **Button**: "Reset Password"
- **Use Case**: Forgotten password

## Configuration

### Environment Variables Required
Add these to your `.env` file:

```bash
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

### Gmail App Password Setup
1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password for "Mail"
4. Use that password in `EMAIL_PASS`

## Function Parameters

All authentication functions accept these parameters:

```python
def send_auth_link(email, send_via_email=True):
    """
    Args:
        email (str): Recipient email address
        send_via_email (bool): If True, sends email. If False, only generates link

    Returns:
        str: The authentication link (or None if error)
    """
```

## Usage Examples

### Basic Usage (Send Email)
```python
from firebase_auth_client import send_email_login

# This will generate AND send the email
link = send_email_login("user@example.com")
```

### Generate Link Only (No Email)
```python
from firebase_auth_client import send_email_login

# This will only generate the link, not send email
link = send_email_login("user@example.com", send_via_email=False)
print(f"Link: {link}")
```

### Error Handling
```python
from firebase_auth_client import send_password_reset_email

link = send_password_reset_email("user@example.com")
if link:
    print("Password reset email sent successfully!")
else:
    print("Failed to send password reset email")
```

## Integration with Flask App

### Add Password Reset Route
```python
from firebase_auth_client import send_password_reset_email

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email required"}), 400

    link = send_password_reset_email(email)
    if link:
        return jsonify({"success": True, "message": "Password reset email sent"}), 200
    else:
        return jsonify({"error": "Failed to send email"}), 500
```

### Add Email Login Route
```python
from firebase_auth_client import send_email_login

@app.route("/request-login-link", methods=["POST"])
def request_login_link():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email required"}), 400

    link = send_email_login(email)
    if link:
        return jsonify({"success": True, "message": "Sign-in link sent to your email"}), 200
    else:
        return jsonify({"error": "Failed to send email"}), 500
```

## Security Features

### Link Expiration
- All authentication links expire after **1 hour**
- Displayed in email footer for transparency

### Action Code Settings
```python
action_code_settings = auth.ActionCodeSettings(
    url='https://cabw-black-electives-app.web.app/login',
    handle_code_in_app=True
)
```

- **url**: Where users are redirected after clicking the link
- **handle_code_in_app**: Process the authentication code in the app

### Email Security
- Uses Gmail SMTP with SSL (port 465)
- Credentials stored in environment variables
- No plaintext passwords in code

## Testing

### Test Locally
Uncomment the test line in `firebase_auth_client.py`:

```python
if __name__ == "__main__":
    send_email_login("your-test-email@gmail.com")
```

Then run:
```bash
python firebase_auth_client.py
```

### Check Email Delivery
1. Check spam folder if email doesn't arrive
2. Verify environment variables are set correctly
3. Check console output for error messages
4. Ensure Gmail App Password is valid

## Troubleshooting

### Issue: Email not sending
**Solutions**:
1. Verify `EMAIL_SENDER` and `EMAIL_PASS` in `.env`
2. Check Gmail App Password is correct
3. Ensure 2FA is enabled on Gmail account
4. Check console for specific error messages

### Issue: Link doesn't work
**Solutions**:
1. Verify Firebase configuration matches `action_code_settings.url`
2. Check link hasn't expired (1 hour limit)
3. Ensure Firebase project has Email/Password auth enabled

### Issue: HTML not rendering
**Solutions**:
1. Some email clients block HTML
2. Alternative plain link is provided in email
3. Check if `is_html=True` in `send_email()` call

## Email Template Customization

To customize the email appearance, edit the `create_email_html()` function in `firebase_auth_client.py`:

```python
def create_email_html(link, link_type="verification"):
    # Customize colors, fonts, layout here
    html = f"""
    <!-- Your custom HTML template -->
    """
    return html
```

### Customizable Elements
- Header gradient colors
- Button colors and text
- Font families and sizes
- Footer text and branding
- Email width and spacing

## Admin Notifications

### Notify Admins of New Articles
```python
from firebase_auth_client import send_email
from fire_store_client import get_collection_data

def notify_admins_new_article(article_title):
    admins = get_collection_data("admins")
    admin_emails = [admin.to_dict()['email'] for admin in admins]

    html = f"""
    <h2>New Article Pending Approval</h2>
    <p>A new article has been submitted: <strong>{article_title}</strong></p>
    <a href="https://your-app.com/news">Review Article</a>
    """

    send_email(
        body=html,
        recipients=admin_emails,
        subject="New Article Pending Approval"
    )
```

## Best Practices

1. **Always use `send_via_email=True`** for production
2. **Store sensitive data in `.env`** never in code
3. **Test with your own email first** before sending to users
4. **Handle errors gracefully** and log them
5. **Provide clear instructions** in email body
6. **Keep links valid for limited time** (current: 1 hour)
7. **Use meaningful subject lines** for different email types

## Future Enhancements

1. **Email Templates Library** - Multiple template choices
2. **Localization** - Multi-language support
3. **Email Analytics** - Track open rates and clicks
4. **Scheduled Emails** - Digest notifications
5. **Email Preferences** - Let users opt in/out
6. **Rich Formatting** - Add images and better styling
7. **Mobile Optimization** - Responsive email design
