from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as f:
            f.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    
    # List message IDs in the inbox
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=3).execute()
    messages = results.get('messages', [])
    
    for m in messages:
        msg = service.users().messages().get(
            userId='me', id=m['id'], format='full'
            ).execute() 
        email_from = msg["payload"]["headers"][22]["value"]
        
        plain_part = msg["payload"]["parts"][0]
        encoded_body = plain_part["body"]["data"]

        email_body = base64.urlsafe_b64decode(encoded_body).decode("utf-8")
        
        print(f"{email_from}\n{email_body}\n\n")
        


if __name__ == "__main__":
    main()
