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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
