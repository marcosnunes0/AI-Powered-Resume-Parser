from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials

# Access scope
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Load credentials from token.json file
creds = Credentials.from_authorized_user_file("token.json", SCOPES)

# Build the Google Drive API service
service = build("drive", "v3", credentials=creds)

# ID of the folder you want to list files in
folder_id = "1BrxlOOIjjBgBfoh_zVA_wKTrbanXalOg"

# List files in the folder specified by folder_id
results = service.files().list(
    q=f"'{folder_id}' in parents", fields='files(id, name)'
).execute()

# Get the list of files
files = results.get('files', [])

if not files:
    raise FileNotFoundError('not files in results')
else:
    for file in files:
        
        # Download each file on the drive
        requests = service.files().get_media(fileId=file['id'])
        file_path = f'./CVs/{file['name']}' # Defines the path where to save the file
        with open(file_path, 'wb') as file:
            downloader = MediaIoBaseDownload(file, requests)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")