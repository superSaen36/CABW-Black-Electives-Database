import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fire_store_client import add_data, update_data

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly","https://www.googleapis.com/auth/documents.readonly"]

# The ID and range of a sample spreadsheet.
ELECTIVES_SPREADSHEET_ID = "1f1ksfl7Y_OIArljXQ2x6jxS9dJVAhgMuogYr_5DLPY4"
SAMPLE_RANGE_NAME = "Electeds!A:N"

def get_credentials():
        """
        Get the data from the electives spreadsheet
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

def get_document_id(link):
    """
    Get the document id from the link
    """
    return link.split("/d/")[1].split("/edit")[0]

def spreadsheet_service(creds):
        try:
            service = build("sheets", "v4", credentials=creds)

            # Call the Sheets API
            result = (
                service.spreadsheets().get(
                    spreadsheetId=ELECTIVES_SPREADSHEET_ID,
                    ranges=[SAMPLE_RANGE_NAME],
                    fields="sheets.data.rowData.values.textFormatRuns,sheets.data.rowData.values.formattedValue"
                ).execute()
            )
            return result
        except HttpError as err:
            print(err)
            return None
        
def doc_service(creds, document_id):
    try:
        service = build("docs", "v1", credentials=creds)
        document = service.documents().get(documentId=document_id).execute()

        print(f"The title of the document is: {document.get('title')}")
        paragraphs, images = extract_paragraphs_and_images(document)
        print("Paragraphs:")
        for p in paragraphs:
            print(p)
        print("Images:")
        for img in images:
            print(img)
        return paragraphs, images
    except HttpError as err:
        print(err)
        return None, None

def extract_paragraphs_and_images(document):
    paragraphs = []
    images = []

    content = document.get('body', {}).get('content', [])
    inline_objects = document.get('inlineObjects', {})
    print("content", content)
    
    for element in content:
        # Extract paragraphs
        if 'paragraph' in element:
            para_text = ''
            for elem in element['paragraph'].get('elements', []):
                text_run = elem.get('textRun')
                if text_run:
                    para_text += text_run.get('content', '')
                
                # Check for images within paragraph elements
                if 'inlineObjectElement' in elem:
                    inline_object_id = elem['inlineObjectElement'].get('inlineObjectId')
                    if inline_object_id and inline_object_id in inline_objects:
                        embedded_object = inline_objects[inline_object_id].get('inlineObjectProperties', {}).get('embeddedObject', {})
                        image_uri = embedded_object.get('imageProperties', {}).get('contentUri')
                        if image_uri:
                            images.append(image_uri)
            
            if para_text.strip():
                paragraphs.append(para_text.strip())

        # Extract images at top level (if any)
        if 'inlineObjectElement' in element:
            inline_object_id = element['inlineObjectElement'].get('inlineObjectId')
            if inline_object_id and inline_object_id in inline_objects:
                embedded_object = inline_objects[inline_object_id].get('inlineObjectProperties', {}).get('embeddedObject', {})
                image_uri = embedded_object.get('imageProperties', {}).get('contentUri')
                if image_uri:
                    images.append(image_uri)

    return paragraphs, images

def main():
    creds = get_credentials()
    values = spreadsheet_service(creds)
    if not values:
        print("No data found.")
        return

    row_data = values.get("sheets")[0].get("data")[0].get("rowData")
    
    # Get column names from header row
    header_cells = row_data[0].get("values", [])
    column_names = [cell.get("formattedValue", "") for cell in header_cells]
    
    for row in row_data[1:]:  # skip header
        cells = row.get("values", [])
        #print("cells", cells)
        if cells:
            # Create dictionary with column names as keys and cell values as values
            row_dict = {}
            for i, cell in enumerate(cells):
                if i < len(column_names):
                    row_dict[column_names[i]] = cell.get("formattedValue", "")
            
            last_cell = cells[-1]
            print("last_cell", last_cell)
            link = last_cell.get("formattedValue", None)
            if link and "http" in link:
                document_id = get_document_id(link)
                print("document_id", document_id)
                paragraphs, images = doc_service(creds, document_id)
                print("paragraphs", paragraphs)
                print("images", images)
                row_dict["bio"] = paragraphs
                row_dict["image"] = images
                print("row_dict", row_dict)
                add_data(row_dict)


if __name__ == "__main__":
  main()