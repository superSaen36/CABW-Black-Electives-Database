import firebase_admin
from firebase_admin import firestore, auth
from firebase_admin import credentials
from email_client import send_email

# Check if Firebase is already initialized, if not initialize it
try:
    firebase_admin.get_app()
except ValueError:
    # App doesn't exist, initialize it
    cred = credentials.Certificate("firebase_service_account_key.json")
    firebase_admin.initialize_app(cred)

action_code_settings = auth.ActionCodeSettings(
    url='https://cabw-black-electives-app.web.app/login',
    handle_code_in_app=True
)

def create_email_html(link, link_type="verification"):
    """Create an HTML email template for authentication links"""
    if link_type == "verification":
        title = "Verify Your Email"
        message = "Please click the button below to verify your email address:"
        button_text = "Verify Email"
    elif link_type == "signin":
        title = "Sign In to Your Account"
        message = "Click the button below to sign in to your California Black Power Book account:"
        button_text = "Sign In"
    elif link_type == "reset":
        title = "Reset Your Password"
        message = "Click the button below to reset your password:"
        button_text = "Reset Password"
    else:
        title = "Authentication Link"
        message = "Click the button below to continue:"
        button_text = "Continue"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 40px auto;
                background-color: #ffffff;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px 20px;
                text-align: center;
            }}
            .header h1 {{
                color: white;
                margin: 0;
                font-size: 28px;
                font-weight: 700;
            }}
            .content {{
                padding: 40px 30px;
                text-align: center;
            }}
            .content p {{
                color: #555;
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 30px;
            }}
            .button {{
                display: inline-block;
                padding: 15px 40px;
                background: linear-gradient(135deg, #9c288c 0%, #764ba2 100%);
                color: white !important;
                text-decoration: none;
                border-radius: 25px;
                font-weight: 600;
                font-size: 16px;
                transition: transform 0.3s ease;
            }}
            .button:hover {{
                transform: translateY(-2px);
            }}
            .alternative-link {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e0e0e0;
            }}
            .alternative-link p {{
                font-size: 12px;
                color: #888;
            }}
            .alternative-link a {{
                color: #764ba2;
                word-break: break-all;
            }}
            .footer {{
                background-color: #f9f9f9;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>California Black Power Book</h1>
            </div>
            <div class="content">
                <h2 style="color: #9c288c; margin-bottom: 20px;">{title}</h2>
                <p>{message}</p>
                <a href="{link}" class="button">{button_text}</a>
                <div class="alternative-link">
                    <p>Or copy and paste this link into your browser:</p>
                    <a href="{link}">{link}</a>
                </div>
            </div>
            <div class="footer">
                <p>This link will expire in 1 hour for security purposes.</p>
                <p>If you didn't request this email, please ignore it.</p>
                <p>&copy; 2025 California Black Women's Collective. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def send_auth_link(email, send_via_email=True):
    """Generate and optionally send email verification link"""
    try:
        link = auth.generate_email_verification_link(
            email,
            action_code_settings
        )
        print(f"Email verification link generated: {link}")

        if send_via_email:
            html_body = create_email_html(link, "verification")
            send_email(
                body=html_body,
                recipients=[email],
                subject="Verify Your Email - California Black Power Book"
            )
            print(f"Verification email sent to {email}")

        return link
    except Exception as e:
        print(f"Error generating/sending verification link: {e}")
        return None

def send_email_login(email, send_via_email=True):
    """Generate and send passwordless sign-in link"""
    try:
        link = auth.generate_sign_in_with_email_link(email, action_code_settings)
        print(f"Sign-in link generated: {link}")

        if send_via_email:
            html_body = create_email_html(link, "signin")
            send_email(
                body=html_body,
                recipients=[email],
                subject="Sign In to California Black Power Book"
            )
            print(f"Sign-in email sent to {email}")

        return link
    except Exception as e:
        print(f"Error generating/sending sign-in link: {e}")
        return None

def send_password_reset_email(email, send_via_email=True):
    """Generate and send password reset link"""
    try:
        link = auth.generate_password_reset_link(email, action_code_settings)
        print(f"Password reset link generated: {link}")

        if send_via_email:
            html_body = create_email_html(link, "reset")
            send_email(
                body=html_body,
                recipients=[email],
                subject="Reset Your Password - California Black Power Book"
            )
            print(f"Password reset email sent to {email}")

        return link
    except Exception as e:
        print(f"Error generating/sending password reset link: {e}")
        return None

# Test function - uncomment to test
# if __name__ == "__main__":
#     send_email_login("seanbrhn3@gmail.com")
