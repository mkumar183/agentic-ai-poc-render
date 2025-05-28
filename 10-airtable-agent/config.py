import os
import secrets
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

AIRTABLE_CLIENT_ID = os.getenv("AIRTABLE_CLIENT_ID")
AIRTABLE_CLIENT_SECRET = os.getenv("AIRTABLE_CLIENT_SECRET") # Only if you have one
AIRTABLE_REDIRECT_URI = "http://localhost:8000/callback" # Must match your registered redirect URI
AIRTABLE_AUTHORIZE_URL = "https://airtable.com/oauth2/v1/authorize"
AIRTABLE_TOKEN_URL = "https://airtable.com/oauth2/v1/token"
AIRTABLE_API_BASE_URL = "https://api.airtable.com/v0"
AIRTABLE_SCOPES = "data.records:read data.records:write schema.bases:read"
# Generate a secure secret key if not set in environment
FASTAPI_SECRET_KEY = os.getenv("FASTAPI_SECRET_KEY")