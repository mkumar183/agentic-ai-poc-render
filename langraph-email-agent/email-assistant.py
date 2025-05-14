from typing import Dict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
import base64
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
import uvicorn

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

app = FastAPI()

class EmailProcessor:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo")
        self.service = self._get_gmail_service()
    
    def _get_gmail_service(self):
        """Get Gmail API service."""
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=61495)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def get_labels(self):
        """Get all Gmail labels."""
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return {label['name']: label['id'] for label in labels}

    def fetch_emails(self, max_results: int = 10) -> List[Dict]:
        """Fetch recent emails from Gmail INBOX only."""
        results = self.service.users().messages().list(
            userId='me',
            labelIds=['INBOX'],  # Only fetch emails from INBOX
            maxResults=max_results
        ).execute()
        messages = results.get('messages', [])
        
        email_data = []
        for message in messages:
            msg = self.service.users().messages().get(
                userId='me', 
                id=message['id']
            ).execute()
            
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            
            # # Get email body
            # if 'parts' in msg['payload']:
            #     body = msg['payload']['parts'][0]['body'].get('data', '')
            # else:
            #     body = msg['payload']['body'].get('data', '')
            
            # if body:
            #     body = base64.urlsafe_b64decode(body).decode()
            body = 'test'
            
            email_data.append({
                'id': message['id'],
                'subject': subject,
                'sender': sender,
                'body': body
            })
        
        return email_data

    def classify_email(self, email: Dict) -> str:
        """Classify if an email is spam/marketing."""
        prompt = f"""
        Analyze this email and classify it as either 'spam/marketing' or 'important':
        
        Subject: {email['subject']}
        From: {email['sender']}
        Body: {email['body'][:500]}...
        
        Respond with only 'spam/marketing' or 'important'.
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip().lower()

    def move_to_spam(self, email_id: str) -> bool:
        """Move an email to spam folder."""
        try:
            # Get all labels
            labels = self.get_labels()
            spam_label_id = labels.get('spam-ai-bot')
            
            if not spam_label_id:
                print("Custom label 'spam-ai-bot' not found. Available labels:", list(labels.keys()))
                return False

            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'addLabelIds': [spam_label_id], 'removeLabelIds': ['INBOX']}
            ).execute()
            return True
        except Exception as e:
            print(f"Error moving email to spam: {e}")
            return False

    def process_emails(self):
        """Process emails and move spam to spam folder."""
        print("Fetching emails...")
        emails = self.fetch_emails()
        
        results = []
        for email in emails:
            print(f"\nProcessing email: {email['subject']}")
            classification = self.classify_email(email)
            
            if classification == 'spam/marketing':
                print(f"Moving to spam: {email['subject']}")
                success = self.move_to_spam(email['id'])
                if success:
                    print("Successfully moved to spam")
                    results.append({
                        'subject': email['subject'],
                        'status': 'moved_to_spam',
                        'success': True
                    })
                else:
                    print("Failed to move to spam")
                    results.append({
                        'subject': email['subject'],
                        'status': 'failed_to_move',
                        'success': False
                    })
            else:
                print(f"Keeping in inbox: {email['subject']}")
                results.append({
                    'subject': email['subject'],
                    'status': 'kept_in_inbox',
                    'success': True
                })
        
        return results

@app.get("/")
async def root():
    return {"message": "Email Assistant API is running"}

@app.post("/process-emails")
async def process_emails():
    try:
        processor = EmailProcessor()
        results = processor.process_emails()
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
