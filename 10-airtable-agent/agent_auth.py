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
        """Initialize the Airtable agent with a unique identifier."""
        if not agent_id:
            raise ValueError("agent_id cannot be empty")
            
        self.agent_id = agent_id
        self.credentials_file = f"agent_credentials_{agent_id}.json"
        self.credentials = {
            'access_token': None,
            'refresh_token': None,
            'expires_at': 0
        }
        self._load_credentials()

    def _load_credentials(self) -> None:
        """Load agent credentials from file if they exist."""
        try:
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    loaded_credentials = json.load(f)
                    # Validate required fields
                    if all(key in loaded_credentials for key in ['access_token', 'refresh_token', 'expires_at']):
                        self.credentials = loaded_credentials
                    else:
                        print(f"Warning: Invalid credentials format in {self.credentials_file}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.credentials_file}")
        except Exception as e:
            print(f"Error loading credentials: {str(e)}")

    def _save_credentials(self) -> None:
        """Save agent credentials to file."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.credentials_file) or '.', exist_ok=True)
            
            # Validate credentials before saving
            if not all(key in self.credentials for key in ['access_token', 'refresh_token', 'expires_at']):
                raise ValueError("Invalid credentials format")
                
            with open(self.credentials_file, 'w') as f:
                json.dump(self.credentials, f, indent=2)
        except Exception as e:
            print(f"Error saving credentials: {str(e)}")
            raise

    def set_initial_tokens(self, access_token: str, refresh_token: str, expires_in: int) -> None:
        """Set initial tokens after OAuth authorization."""
        if not all([access_token, refresh_token, expires_in]):
            raise ValueError("All token parameters must be provided")
            
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

            # Update credentials with new tokens
            self.credentials['access_token'] = token_info['access_token']
            self.credentials['refresh_token'] = token_info.get('refresh_token', self.credentials['refresh_token'])
            self.credentials['expires_at'] = time.time() + token_info['expires_in']
            self._save_credentials()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error refreshing token: {str(e)}")
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
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {str(e)}")
            raise

    def list_bases(self) -> Dict[str, Any]:
        """List all accessible Airtable bases."""
        return self.make_authenticated_request('GET', 'meta/bases')

    def list_requisitions(self, base_id: str) -> Dict[str, Any]:
        """List all requisitions in a specific base."""
        if not base_id:
            raise ValueError("base_id cannot be empty")
        return self.make_authenticated_request('GET', f"{base_id}/Requisitions")

    def add_requisition(self, base_id: str, requisition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new requisition to the specified base."""
        if not base_id:
            raise ValueError("base_id cannot be empty")
        if not requisition_data:
            raise ValueError("requisition_data cannot be empty")
            
        data = {
            "records": [{
                "fields": requisition_data
            }]
        }
        return self.make_authenticated_request('POST', f"{base_id}/Leads", json=data)

    def update_requisition(self, base_id: str, record_id: str, requisition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing requisition in the specified base."""
        if not all([base_id, record_id]):
            raise ValueError("base_id and record_id cannot be empty")
        if not requisition_data:
            raise ValueError("requisition_data cannot be empty")
            
        data = {
            "fields": requisition_data
        }
        return self.make_authenticated_request('PATCH', f"{base_id}/Requisitions/{record_id}", json=data)

    def delete_requisition(self, base_id: str, record_id: str) -> Dict[str, Any]:
        """Delete a requisition from the specified base."""
        if not all([base_id, record_id]):
            raise ValueError("base_id and record_id cannot be empty")
        return self.make_authenticated_request('DELETE', f"{base_id}/Requisitions/{record_id}")

# Example usage
if __name__ == "__main__":
    try:
        # Load tokens from file
        with open('airtable_tokens.json', 'r') as f:
            token_info = json.load(f)
        
        # Create an agent instance
        agent = AirtableAgent("my-agent")
        
        # Set initial tokens
        agent.set_initial_tokens(
            access_token=token_info['access_token'],
            refresh_token=token_info['refresh_token'],
            expires_in=token_info['expires_in']
        )
        
        # Test the connection
        print("Testing connection by listing bases...")
        bases = agent.list_bases()
        print("Successfully connected to Airtable!")
        print(f"Found {len(bases.get('bases', []))} bases")
        
    except FileNotFoundError:
        print("Error: airtable_tokens.json not found. Please run get_tokens.py first.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON in airtable_tokens.json")
    except Exception as e:
        print(f"Error: {str(e)}")        