import base64
import secrets
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import requests, json, hashlib
from config import (
    AIRTABLE_CLIENT_ID,
    AIRTABLE_CLIENT_SECRET,
    AIRTABLE_REDIRECT_URI,
    AIRTABLE_AUTHORIZE_URL,
    AIRTABLE_TOKEN_URL
)

# Generate PKCE codes
def generate_pkce_codes():
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the callback URL
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        # Verify state parameter
        received_state = query_components.get('state', [None])[0]
        if received_state != self.server.oauth_state:
            self.send_error(400, "Invalid state parameter")
            return

        if 'code' in query_components:
            code = query_components['code'][0]
            
            # Exchange code for tokens
            token_data = {
                "grant_type": "authorization_code",
                "client_id": AIRTABLE_CLIENT_ID,
                "code": code,
                "redirect_uri": AIRTABLE_REDIRECT_URI,
                "code_verifier": self.server.code_verifier
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
                
                # Store tokens in a file
                with open('airtable_tokens.json', 'w') as f:
                    json.dump(token_info, f, indent=2)
                
                # Send success response to browser
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"""
                <html>
                    <body>
                        <h1>Authentication Successful!</h1>
                        <p>Tokens have been saved to airtable_tokens.json</p>
                        <p>You can now close this window and use the tokens with your agent.</p>
                    </body>
                </html>
                """)
                
                # Shutdown the server after successful authentication
                self.server.should_stop = True
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f"""
                <html>
                    <body>
                        <h1>Error</h1>
                        <p>Failed to get tokens: {str(e)}</p>
                    </body>
                </html>
                """.encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
            <html>
                <body>
                    <h1>Error</h1>
                    <p>No authorization code received</p>
                </body>
            </html>
            """)

class OAuthServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.should_stop = False
        self.code_verifier = None
        self.oauth_state = None

def main():
    # Generate PKCE codes
    code_verifier, code_challenge = generate_pkce_codes()
    
    # Generate state parameter
    oauth_state = secrets.token_urlsafe(32)
    
    # Create authorization URL
    params = {
        "client_id": AIRTABLE_CLIENT_ID,
        "redirect_uri": AIRTABLE_REDIRECT_URI,
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": oauth_state,
        "scope": "data.records:read data.records:write schema.bases:read"
    }
    auth_url = f"{AIRTABLE_AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"
    
    # Start local server to receive callback
    server = OAuthServer(('localhost', 8000), OAuthCallbackHandler)
    server.code_verifier = code_verifier
    server.oauth_state = oauth_state
    
    print("Opening browser for Airtable authorization...")
    webbrowser.open(auth_url)
    
    print("Waiting for authorization callback...")
    while not server.should_stop:
        server.handle_request()
    
    print("Authentication complete! You can now use the agent.")

if __name__ == "__main__":
    main() 