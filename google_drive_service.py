import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If the scopes are modified, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

def get_service():
    creds = None

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

    service = build("drive", "v3", credentials=creds)

    return service

def search_folder_by_name(folder_name, service):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print(f"Folder '{folder_name}' not found.")
        return None
    return items[0]['id']

def create_folder(folder_name, service):
    file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
    return service.files().create(body=file_metadata, fields='id, name').execute()

def upload_file_drive(path, name):
    try:
        service = get_service()
        folder_name = f"Croydon_Jail_images"
        folder_id = search_folder_by_name(folder_name, service)
        if not folder_id:
            folder_id = create_folder(folder_name, service)['id']

        file_metadata = {'name': name}
        if folder_id:
            file_metadata['parents'] = [folder_id]
            
        media = MediaFileUpload(path, mimetype='image/jpg')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        print(f"File ID: {file.get('id')}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file





