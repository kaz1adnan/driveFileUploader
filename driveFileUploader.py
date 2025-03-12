import os
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

folder_id = '179MhtbsTUDmMQy93zMdMV-BsIxJZmBg3'

SCOPES = ['https://www.googleapis.com/auth/drive']

def createConnection():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def uploadFile(filePath, fileName, creds):
    try:
        service = build('drive', 'v3', credentials=creds)  # Fixed undefined 'service'

        file = MediaFileUpload(filePath, resumable=True)

        fileMetadata = {
            'name': fileName,
            'parents': [folder_id]
        }

        file = service.files().create(
            body=fileMetadata,
            media_body=file,
            fields='id'
        ).execute()

        print(f'File "{fileName}" uploaded to Google Drive with ID: {file.get("id")}')

    except HttpError as error:
        print(f'An error occurred while uploading file "{fileName}" to Google Drive: {error}')
        file = None

    return file

def uploadFiles(directoryPath, creds):
    if not os.path.exists(directoryPath):
        print("Directory does not exist!")
        return

    files = os.listdir(directoryPath)

    if not files:
        print("No files found in the directory!")
        return

    for fileName in files:
        filePath = os.path.join(directoryPath, fileName)

        if os.path.isfile(filePath):  # Upload only files, not directories
            uploadFile(filePath, fileName, creds)

creds = createConnection()
directoryPath = r'F:\testFolder'  # Fixed path issue
uploadFiles(directoryPath, creds)
