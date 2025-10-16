import firebase_admin
from firebase_admin import firestore, auth
from firebase_admin import credentials

cred = credentials.Certificate("firebase_service_account_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Generic collection functions with parameterized collection name
def add_data(data, collection="electeds-db"):
    """Add data to a specified collection"""
    print(f"Adding data to {collection}", data)
    doc_ref = db.collection(collection).add(data)
    print(f"Document added with ID: {doc_ref[1].id}")
    print("data added successfully")
    return doc_ref[1].id

def get_data(collection="electeds"):
    """Get all documents from a specified collection"""
    return db.collection(collection).get()

def get_electeds_data():
    """Get all elected officials data (legacy function for backward compatibility)"""
    docs = db.collection("electeds-db").get()
    for doc in docs:
        print(f"Document ID: {doc.id}")
        print(f"Document data: {doc.to_dict()}")
    return docs

def get_collection_data(collection):
    """Get all data from a specified collection"""
    docs = db.collection(collection).get()
    return docs

def update_data(data, collection="electeds"):
    """Update data in a specified collection"""
    db.collection(collection).update(data)

def get_document_by_id(collection, doc_id):
    """Get a specific document by ID from a collection"""
    try:
        doc = db.collection(collection).document(doc_id).get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        print(f"Error getting document: {e}")
        return None

def update_document_by_id(collection, doc_id, data):
    """Update a specific document by ID in a collection"""
    try:
        db.collection(collection).document(doc_id).update(data)
        print(f"Document {doc_id} updated successfully in {collection}")
        return True
    except Exception as e:
        print(f"Error updating document: {e}")
        return False

def delete_document_by_id(collection, doc_id):
    """Delete a specific document by ID from a collection"""
    try:
        db.collection(collection).document(doc_id).delete()
        print(f"Document {doc_id} deleted successfully from {collection}")
        return True
    except Exception as e:
        print(f"Error deleting document: {e}")
        return False

# Admin-specific functions
def add_admin(email, user_name, phone=None, mfa_enabled=False):
    """Add an admin to the admins collection"""
    admin_data = {
        "email": email,
        "user_name": user_name,
        "phone": phone,
        "mfa_enabled": mfa_enabled,
        "created_at": firestore.SERVER_TIMESTAMP
    }
    return add_data(admin_data, collection="admins")

def get_admin_by_email(email):
    """Check if a user is an admin by email"""
    try:
        admins = db.collection("admins").where("email", "==", email).get()
        if admins:
            return admins[0].to_dict()
        return None
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return None

def is_admin(email):
    """Check if a user is an admin"""
    admin = get_admin_by_email(email)
    return admin is not None

# Articles collection functions
def add_article(title, link, published, source, approved=False):
    """Add a news article to the articles collection"""
    article_data = {
        "title": title,
        "link": link,
        "published": published,
        "source": source,
        "approved": approved,
        "created_at": firestore.SERVER_TIMESTAMP
    }
    return add_data(article_data, collection="articles")

def get_all_articles():
    """Get all articles regardless of approval status"""
    try:
        docs = db.collection("articles").order_by("created_at", direction=firestore.Query.DESCENDING).get()
        articles = []
        for doc in docs:
            article = doc.to_dict()
            article['id'] = doc.id
            articles.append(article)
        return articles
    except Exception as e:
        print(f"Error getting articles: {e}")
        return []

def get_approved_articles():
    """Get only approved articles"""
    try:
        docs = db.collection("articles").where("approved", "==", True).order_by("created_at", direction=firestore.Query.DESCENDING).get()
        articles = []
        for doc in docs:
            article = doc.to_dict()
            article['id'] = doc.id
            articles.append(article)
        return articles
    except Exception as e:
        print(f"Error getting approved articles: {e}")
        return []

def approve_article(article_id):
    """Approve an article"""
    return update_document_by_id("articles", article_id, {"approved": True})

def disapprove_article(article_id):
    """Disapprove an article"""
    return update_document_by_id("articles", article_id, {"approved": False})

def create_user(email, password, display_name=None, send_verification=True):
    """
    Create a new Firebase user and optionally send verification email

    Args:
        email (str): User's email address
        password (str): User's password
        display_name (str): Optional display name
        send_verification (bool): Whether to send verification email (default: True)

    Returns:
        user object if successful, None otherwise
    """
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        print(f"User created successfully: {user.uid} - {email}")

        # Send verification email if requested
        if send_verification:
            try:
                from firebase_auth_client import send_auth_link
                link = send_auth_link(email, send_via_email=True)
                if link:
                    print(f"Verification email sent to {email}")
                else:
                    print(f"Failed to send verification email to {email}")
            except Exception as email_error:
                print(f"Error sending verification email: {email_error}")
                # Don't fail user creation if email fails

        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def verify_id_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None

def get_user_by_email(email):
    try:
        user = auth.get_user_by_email(email)
        return user
    except Exception as e:
        print(f"Error getting user: {e}")
        return None
