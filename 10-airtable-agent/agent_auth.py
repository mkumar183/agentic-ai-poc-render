import json
import os
import time
import base64
from typing import Optional, Dict, Any
import requests
from config import (
    AIRTABLE_CLIENT_ID,
    AIRTABLE_CLIENT_SECRET,
    AIRTABLE_TOKEN_URL,
    AIRTABLE_API_BASE_URL
)

class AirtableAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.credentials_file = f"agent_credentials_{agent_id}.json"
        self._load_credentials()

    def _load_credentials(self) -> None:
        """Load agent credentials from file if they exist."""
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r') as f:
                self.credentials = json.load(f)
        else:
            self.credentials = {
                'access_token': None,
                'refresh_token': None,
                'expires_at': 0
            }

    def _save_credentials(self) -> None:
        """Save agent credentials to file."""
        with open(self.credentials_file, 'w') as f:
            json.dump(self.credentials, f)

    def set_initial_tokens(self, access_token: str, refresh_token: str, expires_in: int) -> None:
        """Set initial tokens after OAuth authorization."""
        self.credentials = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_at': time.time() + expires_in
        }
        self._save_credentials()

    def _refresh_token(self) -> bool:
        """Refresh the access token using the refresh token."""
        if not self.credentials.get('refresh_token'):
            return False

        token_data = {
            "grant_type": "refresh_token",
            "client_id": AIRTABLE_CLIENT_ID,
            "refresh_token": self.credentials['refresh_token'],
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if AIRTABLE_CLIENT_SECRET:
            credentials = f"{AIRTABLE_CLIENT_ID}:{AIRTABLE_CLIENT_SECRET}"
            encoded_credentials = base64.urlsafe_b64encode(credentials.encode('utf-8')).decode('utf-8')
            headers["Authorization"] = f"Basic {encoded_credentials}"

        try:
            response = requests.post(AIRTABLE_TOKEN_URL, data=token_data, headers=headers)
            response.raise_for_status()
            token_info = response.json()

            self.credentials['access_token'] = token_info['access_token']
            self.credentials['refresh_token'] = token_info.get('refresh_token', self.credentials['refresh_token'])
            self.credentials['expires_at'] = time.time() + token_info['expires_in']
            self._save_credentials()
            return True
        except requests.exceptions.RequestException:
            return False

    def get_valid_token(self) -> Optional[str]:
        """Get a valid access token, refreshing if necessary."""
        if not self.credentials.get('access_token'):
            return None

        # Check if token needs refresh (5 minutes buffer)
        if time.time() >= self.credentials['expires_at'] - 300:
            if not self._refresh_token():
                return None

        return self.credentials['access_token']

    def make_authenticated_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an authenticated request to Airtable API."""
        token = self.get_valid_token()
        if not token:
            raise Exception("No valid authentication token available")

        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f"Bearer {token}"
        kwargs['headers'] = headers

        url = f"{AIRTABLE_API_BASE_URL}/{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def list_bases(self) -> Dict[str, Any]:
        """List all accessible Airtable bases."""
        return self.make_authenticated_request('GET', 'meta/bases')

    def list_leads(self, base_id: str) -> Dict[str, Any]:
        """List all leads in a specific base."""
        return self.make_authenticated_request('GET', f"{base_id}/Leads")

    def add_lead(self, base_id: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new lead to the specified base."""
        data = {
            "records": [{
                "fields": lead_data
            }]
        }
        return self.make_authenticated_request('POST', f"{base_id}/Leads", json=data)

    def update_lead(self, base_id: str, record_id: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing lead in the specified base."""
        data = {
            "fields": lead_data
        }
        return self.make_authenticated_request('PATCH', f"{base_id}/Leads/{record_id}", json=data)

    def delete_lead(self, base_id: str, record_id: str) -> Dict[str, Any]:
        """Delete a lead from the specified base."""
        return self.make_authenticated_request('DELETE', f"{base_id}/Leads/{record_id}")

# Example usage
if __name__ == "__main__":
    # Create an agent instance
    agent = AirtableAgent("my-agent")
    
    # If you need to initialize the agent with tokens (do this once)
    # You can get these tokens from your OAuth flow or manually
    agent.set_initial_tokens(
        access_token="your_access_token",
        refresh_token="your_refresh_token",
        expires_in=3600  # Token expiration time in seconds
    )
    
    try:
        # List all bases
        print("Listing bases...")
        bases = agent.list_bases()
        print("Available bases:", bases)
        
        # List leads in a specific base
        base_id = "app1UpIBhCPTYd7zJ"  # Replace with your base ID
        print(f"\nListing leads in base {base_id}...")
        leads = agent.list_leads(base_id)
        print("Leads:", leads)
        
        # Add a new lead
        print("\nAdding a new lead...")
        new_lead = agent.add_lead(base_id, {
            "Name": "John Doe",
            "Email": "john@example.com",
            "Phone": "123-456-7890",
            "Status": "New"
        })
        print("New lead added:", new_lead)
        
        # Update a lead (if you have a record ID)
        if leads.get('records'):
            record_id = leads['records'][0]['id']
            print(f"\nUpdating lead {record_id}...")
            updated_lead = agent.update_lead(base_id, record_id, {
                "Status": "Contacted"
            })
            print("Lead updated:", updated_lead)
            
            # Delete the lead
            print(f"\nDeleting lead {record_id}...")
            delete_result = agent.delete_lead(base_id, record_id)
            print("Lead deleted:", delete_result)
            
    except Exception as e:
        print(f"Error: {str(e)}")        