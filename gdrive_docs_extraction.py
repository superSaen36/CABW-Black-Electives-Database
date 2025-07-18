import os
import base64
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

# CONFIGURATION
SCOPES = [
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]
SERVICE_ACCOUNT_FILE = 'black-electives-database-f8978e925e6e.json'
FOLDER_NAME = "Black Elective's Database/Headshots and Bios"

# Authenticate
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
docs_service = build('docs', 'v1', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

# FUNCTIONS

def list_google_docs_in_folder(drive_service, folder_name):
    # Find folder ID
    query = (
        f"name = '{folder_name}' and "
        "mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    )
    response = drive_service.files().list(
        q=query, spaces='drive', fields='files(id, name)'
    ).execute()
    folders = response.get('files', [])

    if not folders:
        print(f"No folder named '{folder_name}' found.")
        return []

    folder_id = folders[0]['id']

    # List Google Docs in folder
    query = (
        f"'{folder_id}' in parents and "
        "mimeType = 'application/vnd.google-apps.document' and trashed = false"
    )
    docs_response = drive_service.files().list(
        q=query, spaces='drive', fields='files(id, name)', pageSize=1000
    ).execute()

    docs_files = docs_response.get('files', [])

    for doc in docs_files:
        print(f"Found Document: {doc['name']} (ID: {doc['id']})")

    return [doc['id'] for doc in docs_files]


def extract_doc_content(document_id, docs_service):
    document = docs_service.documents().get(documentId=document_id).execute()
    paragraphs = []
    images = []

    for element in document.get('body', {}).get('content', []):
        if 'paragraph' in element:
            text_run = ''
            for elem in element['paragraph'].get('elements', []):
                if 'textRun' in elem:
                    text_run += elem['textRun'].get('content', '')
            if text_run.strip():
                paragraphs.append(text_run.strip())

        if 'inlineObjectElement' in element:
            inline_object_id = element['inlineObjectElement']['inlineObjectId']
            inline_object = document['inlineObjects'][inline_object_id]
            embedded_object = inline_object['inlineObjectProperties']['embeddedObject']

            if 'imageProperties' in embedded_object:
                content_uri = embedded_object['imageProperties']['contentUri']
                response = requests.get(content_uri)
                if response.status_code == 200:
                    image_data = base64.b64encode(response.content).decode('utf-8')
                    images.append(image_data)

    return paragraphs, images


# MAIN EXECUTION

# Step 1: List document IDs from folder
doc_ids = list_google_docs_in_folder(drive_service, FOLDER_NAME)

# Step 2: Process each document
for doc_id in doc_ids:
    print(f"\nProcessing Document ID: {doc_id}")
    paragraphs, images = extract_doc_content(doc_id, docs_service)

    print("\nParagraphs Found:")
    for para in paragraphs:
        print(para)
        print('-' * 50)

    print(f"\nExtracted {len(images)} images.")

    # Optional: Save images as files
    for idx, img_data in enumerate(images):
        image_filename = f"{doc_id}_image_{idx+1}.png"
        with open(image_filename, 'wb') as img_file:
            img_file.write(base64.b64decode(img_data))
        print(f"Saved image: {image_filename}")
