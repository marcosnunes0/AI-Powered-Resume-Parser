import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Set the access scope you need
# These scopes allow reading and modifying files in Google Drive
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.metadata.readonly"
]

# Initialize the credentials variable
creds = None

# Check if the token.json file exists in the current directory
# This file stores the access credentials
if os.path.exists('token.json'):
    # If it exists, load the credentials from the token.json file
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    print('Credentials loaded from token.json file.')

# Check if credentials do not exist or are invalid/expired
if not creds or not creds.valid:
    # If credentials exist but are expired and can be renewed
    if creds and creds.expired and creds.refresh_token:
        # Renew credentials using refresh token
        creds.refresh(Request())
        print('Credentials renewed successfully.')
    else:
        # If there are no valid credentials, start the OAuth authorization flow
        print('Starting OAuth authorization flow...')
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0) # Run the local server for authorization
        print('Authorization completed.')

    # Save renewed or new credentials to the token.json file
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
        print('Credentials saved to token.json file.')