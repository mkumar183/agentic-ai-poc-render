from typing import Dict, List, Annotated, TypedDict
from langgraph.graph import Graph, StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
import base64
from datetime import datetime
from fastapi import FastAPI, HTTPException
import uvicorn
import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama

# Define the state
class EmailState(TypedDict):
    emails: List[Dict]
    processed_emails: List[Dict]
    current_email: Dict
    classification: str
    action_taken: bool

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

app = FastAPI()

class EmailProcessor:
    def __init__(self):
        # self.llm = ChatOpenAI(model="gpt-3.5-turbo")
        self.llm = ChatOpenAI(model="tinyllama")
        self.service = self._get_gmail_service()
        self.graph = self._build_graph()
    
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

    def _build_graph(self) -> Graph:
        """Build the LangGraph for email processing."""
        
        # Define nodes
        def fetch_emails(state: EmailState) -> EmailState:
            """Fetch emails from INBOX."""
            print("DEBUG: Fetching emails from INBOX...")
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['INBOX'],
                maxResults=1
            ).execute()
            messages = results.get('messages', [])
            print(f"DEBUG: Found {len(messages)} messages")
            
            emails = []
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id']
                ).execute()
                
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                print('msg:', msg)
                
                # Get email body
                if 'parts' in msg['payload']:
                    body = msg['payload']['parts'][0]['body'].get('data', '')
                else:
                    body = msg['payload']['body'].get('data', '')
                
                if body:
                    body = base64.urlsafe_b64decode(body).decode()
            
                
                emails.append({
                    'id': message['id'],
                    'subject': subject,
                    'sender': sender,                    
                    'body'  : body
                })
            print(f"DEBUG: Processed {len(emails)} emails")
            return {"emails": emails, "processed_emails": [], "current_email": None, "classification": None, "action_taken": False}

        def classify_email(state: EmailState) -> EmailState:
            """Classify the current email."""
            print(f"DEBUG: Classifying email: {state['current_email']['subject']}")
            email = state["current_email"]
            prompt = f"""
            Analyze this email and classify it as either 'spam/marketing' or 'important':
            
            Subject: {email['subject']}
            From: {email['sender']}
            Body: {email['body']}
            Respond with only 'spam/marketing' or 'important'.
            """
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            classification = response.content.strip().lower()
            print(f"DEBUG: Classification result: {classification}")
            
            return {**state, "classification": classification}

        # this does not work well yet classification is not good. need to improve it. TODO: improve it.
        def classify_email_ollama(state: EmailState) -> EmailState:
            """Classify the current email using Ollama tinylama model."""
            print(f"DEBUG: [Ollama] Classifying email: {state['current_email']['subject']}")
            email = state["current_email"]
            prompt = f"""
            Analyze this email and classify it as either 'spam/marketing' or 'important':
            
            Subject: {email['subject']}
            From: {email['sender']}
            Body: {email['body']}
            Respond with only 'spam/marketing' or 'important'.
            """
            print(f"DEBUG: [Ollama] Prompt: {prompt}")
            ollama_llm = ChatOllama(model="tinyllama")
            response = ollama_llm.invoke([HumanMessage(content=prompt)])
            classification = response.content.strip().lower()
            print(f"DEBUG: [Ollama] Classification result: {classification}")
            return {**state, "classification": classification}


        def take_action(state: EmailState) -> EmailState:
            """Take action based on classification."""
            print(f"DEBUG: Taking action for email: {state['current_email']['subject']}")
            if state["classification"] == 'spam/marketing':
                print("DEBUG: Moving email to spam")
                # Move to spam
                labels = self.get_labels()
                spam_label_id = labels.get('spam-ai-bot')
                
                if spam_label_id:
                    self.service.users().messages().modify(
                        userId='me',
                        id=state["current_email"]["id"],
                        body={'addLabelIds': [spam_label_id], 'removeLabelIds': ['INBOX']}
                    ).execute()
                    print("DEBUG: Successfully moved email to spam")
                else:
                    print("DEBUG: Warning - spam label not found")
            
            processed = state["processed_emails"]
            processed.append({
                **state["current_email"],
                "classification": state["classification"],
                "action_taken": True
            })
            print(f"DEBUG: Added email to processed list. Total processed: {len(processed)}")
            
            return {**state, "processed_emails": processed, "action_taken": True}

        def should_continue(state: EmailState) -> Dict:
            """Determine if we should continue processing emails."""
            remaining = len(state["emails"])
            print(f"DEBUG: Checking if should continue. Remaining emails: {remaining}")
            if not state["emails"]:
                print("DEBUG: No more emails to process, ending")
                return {"next": "end"}
            print("DEBUG: More emails to process, continuing")
            return {"next": "continue"}

        def get_next_email(state: EmailState) -> EmailState:
            """Get the next email to process."""
            emails = state["emails"]
            current = emails.pop(0)
            print(f"DEBUG: Getting next email. Subject: {current['subject']}")
            return {**state, "emails": emails, "current_email": current}


        # Build the graph
        workflow = StateGraph(EmailState)

        # Add nodes
        workflow.add_node("fetch_emails", fetch_emails)
        workflow.add_node("classify_email", classify_email)
        # workflow.add_node("classify_email", classify_email_ollama)
        workflow.add_node("take_action", take_action)
        workflow.add_node("get_next_email", get_next_email)
        workflow.add_node("should_continue", should_continue)

        # Add edges
        workflow.add_edge("fetch_emails", "get_next_email")
        workflow.add_edge("get_next_email", "classify_email")
        workflow.add_edge("classify_email", "take_action")
        workflow.add_edge("take_action", "should_continue")

        # Add conditional edges
        workflow.add_conditional_edges(
            "should_continue",
            lambda x: x["next"],  # Extract the "next" value from the dictionary
            {
                "continue": "get_next_email",
                "end": END
            }
        )

        # Set entry point
        workflow.set_entry_point("fetch_emails")

        return workflow.compile()

    def process_emails(self):
        """Process emails using the LangGraph workflow."""
        print("DEBUG: Starting email processing workflow...")
        
        # Initialize empty state
        initial_state = {
            "emails": [],
            "processed_emails": [],
            "current_email": None,
            "classification": None,
            "action_taken": False
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        print(f"DEBUG: Workflow completed. Processed {len(result['processed_emails'])} emails")
        return result["processed_emails"]

    def find_subscription_emails(self, max_results=100):
        """Find emails that are likely subscriptions."""
        print("DEBUG: Searching for subscription emails...")
        
        # Search for common subscription-related terms
        query = "category:promotions OR (unsubscribe OR subscription OR newsletter OR marketing)"
        results = self.service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        subscription_emails = []
        
        for message in messages:
            msg = self.service.users().messages().get(
                userId='me', 
                id=message['id']
            ).execute()
            
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            
            # Get email body
            if 'parts' in msg['payload']:
                body = msg['payload']['parts'][0]['body'].get('data', '')
            else:
                body = msg['payload']['body'].get('data', '')
            
            if body:
                body = base64.urlsafe_b64decode(body).decode()
            
            # Extract unsubscribe links
            unsubscribe_links = self._extract_unsubscribe_links(body)
            
            subscription_emails.append({
                'id': message['id'],
                'subject': subject,
                'sender': sender,
                'unsubscribe_links': unsubscribe_links
            })
        
        return subscription_emails

    def _extract_unsubscribe_links(self, html_content):
        """Extract unsubscribe links from email content."""
        soup = BeautifulSoup(html_content, 'html.parser')
        unsubscribe_links = []
        
        # Look for common unsubscribe link patterns
        patterns = [
            'unsubscribe',
            'opt-out',
            'preferences',
            'subscription',
            'manage preferences',
            'email preferences'
        ]
        
        for link in soup.find_all('a'):
            href = link.get('href', '')
            text = link.get_text().lower()
            
            if any(pattern in text.lower() or pattern in href.lower() for pattern in patterns):
                unsubscribe_links.append({
                    'text': text,
                    'url': href
                })
        
        return unsubscribe_links

    def unsubscribe_from_email(self, email_data):
        """Attempt to unsubscribe from an email subscription."""
        print(f"DEBUG: Attempting to unsubscribe from: {email_data['sender']}")
        
        for link in email_data['unsubscribe_links']:
            try:
                # Validate URL
                parsed_url = urlparse(link['url'])
                if not parsed_url.scheme or not parsed_url.netloc:
                    print(f"DEBUG: Invalid URL: {link['url']}")
                    continue
                
                # Make the unsubscribe request
                response = requests.get(link['url'], allow_redirects=True)
                
                if response.status_code == 200:
                    print(f"DEBUG: Successfully unsubscribed from {email_data['sender']}")
                    return True
                else:
                    print(f"DEBUG: Failed to unsubscribe. Status code: {response.status_code}")
            
            except Exception as e:
                print(f"DEBUG: Error unsubscribing: {str(e)}")
        
        return False

    def process_subscriptions(self):
        """Process and unsubscribe from email subscriptions."""
        print("DEBUG: Starting subscription processing...")
        
        # Find subscription emails
        subscription_emails = self.find_subscription_emails()
        print(f"DEBUG: Found {len(subscription_emails)} potential subscription emails")
        
        results = []
        for email in subscription_emails:
            print(f"\nProcessing subscription from: {email['sender']}")
            print(f"Subject: {email['subject']}")
            
            if email['unsubscribe_links']:
                print("Found unsubscribe links:")
                for link in email['unsubscribe_links']:
                    print(f"- {link['text']}: {link['url']}")
                
                success = self.unsubscribe_from_email(email)
                results.append({
                    'sender': email['sender'],
                    'subject': email['subject'],
                    'unsubscribe_success': success
                })
            else:
                print("No unsubscribe links found")
                results.append({
                    'sender': email['sender'],
                    'subject': email['subject'],
                    'unsubscribe_success': False,
                    'reason': 'No unsubscribe links found'
                })
        
        return results

@app.get("/")
async def root():
    return {"message": "Email Assistant API is running"}

@app.post("/process-emails")
async def process_emails():
    try:
        print("DEBUG: Starting /process-emails endpoint")
        processor = EmailProcessor()
        results = processor.process_emails()
        print(f"DEBUG: Successfully processed {len(results)} emails")
        return {"status": "success", "results": results}
    except Exception as e:
        print(f"DEBUG: Error in process_emails: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-subscriptions")
async def process_subscriptions():
    try:
        print("DEBUG: Starting /process-subscriptions endpoint")
        processor = EmailProcessor()
        results = processor.process_subscriptions()
        print(f"DEBUG: Successfully processed {len(results)} subscriptions")
        return {"status": "success", "results": results}
    except Exception as e:
        print(f"DEBUG: Error in process_subscriptions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
