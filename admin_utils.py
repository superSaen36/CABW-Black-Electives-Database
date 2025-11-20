"""
Utility script to manage admins in the Firestore database.
Usage:
    python admin_utils.py add <email> <user_name> [--phone <phone>] [--mfa]
    python admin_utils.py list
    python admin_utils.py check <email>
"""

import sys
from fire_store_client import add_admin, get_admin_by_email, get_collection_data

def add_admin_user(email, user_name, phone=None, mfa_enabled=False):
    """Add a new admin to the database"""
    try:
        # Check if admin already exists
        existing_admin = get_admin_by_email(email)
        if existing_admin:
            print(f"Admin with email {email} already exists!")
            return False

        # Add the admin
        admin_id = add_admin(email, user_name, phone, mfa_enabled)
        print(f"Successfully added admin: {user_name} ({email})")
        print(f"Admin ID: {admin_id}")
        print(f"MFA Enabled: {mfa_enabled}")
        return True
    except Exception as e:
        print(f"Error adding admin: {e}")
        return False

def list_admins():
    """List all admins in the database"""
    try:
        admins = get_collection_data("admins")
        if not admins:
            print("No admins found in the database.")
            return

        print("\n=== Current Admins ===")
        for idx, admin_doc in enumerate(admins, 1):
            admin = admin_doc.to_dict()
            print(f"\n{idx}. {admin.get('user_name', 'N/A')}")
            print(f"   Email: {admin.get('email', 'N/A')}")
            print(f"   Phone: {admin.get('phone', 'N/A')}")
            print(f"   MFA Enabled: {admin.get('mfa_enabled', False)}")
            print(f"   Created: {admin.get('created_at', 'N/A')}")
    except Exception as e:
        print(f"Error listing admins: {e}")

def check_admin(email):
    """Check if a user is an admin"""
    try:
        admin = get_admin_by_email(email)
        if admin:
            print(f"\n✓ {email} is an admin")
            print(f"  Name: {admin.get('user_name', 'N/A')}")
            print(f"  Phone: {admin.get('phone', 'N/A')}")
            print(f"  MFA Enabled: {admin.get('mfa_enabled', False)}")
        else:
            print(f"\n✗ {email} is not an admin")
    except Exception as e:
        print(f"Error checking admin status: {e}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 4:
            print("Usage: python admin_utils.py add <email> <user_name> [--phone <phone>] [--mfa]")
            return

        email = sys.argv[2]
        user_name = sys.argv[3]
        phone = None
        mfa_enabled = False

        # Parse optional arguments
        i = 4
        while i < len(sys.argv):
            if sys.argv[i] == "--phone" and i + 1 < len(sys.argv):
                phone = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--mfa":
                mfa_enabled = True
                i += 1
            else:
                i += 1

        add_admin_user(email, user_name, phone, mfa_enabled)

    elif command == "list":
        list_admins()

    elif command == "check":
        if len(sys.argv) < 3:
            print("Usage: python admin_utils.py check <email>")
            return
        email = sys.argv[2]
        check_admin(email)

    else:
        print(f"Unknown command: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
