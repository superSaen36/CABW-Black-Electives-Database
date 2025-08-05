import firebase_admin
from firebase_admin import firestore, auth
from firebase_admin import credentials

cred = credentials.Certificate("firebase_service_account_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_data(data):
    print("data", data)
    doc_ref = db.collection("electeds-db").add(data)
    print(f"Document added with ID: {doc_ref[1].id}")
    print("data added successfully")

def get_data():
    return db.collection("electeds").get()

def get_electeds_data():
    docs = db.collection("electeds-db").get()
    for doc in docs:
        print(f"Document ID: {doc.id}")
        print(f"Document data: {doc.to_dict()}")
    return docs

def update_data(data):
    db.collection("electeds").update(data)

def create_user(email, password, display_name=None):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        print(f"User created: {user}")
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

