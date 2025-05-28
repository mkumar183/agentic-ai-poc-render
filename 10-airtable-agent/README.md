# Airtable Agent Integration
This project provides a secure and automated way to interact with Airtable using an agent-based approach. The agent maintains persistent authentication and can perform CRUD operations on Airtable bases without requiring repeated user authorization.

## Prerequisites
- Python 3.7+
- An Airtable account
- Airtable OAuth application credentials

## Setup Instructions

### 1. Create Airtable OAuth Application
1. Go to [Airtable OAuth Apps](https://airtable.com/create/oauth)
2. Click "Create a new OAuth integration"
3. Fill in the application details:
   - Name: Your application name
   - Redirect URI: `http://localhost:8000/callback`
   - Scopes: Select the required permissions:
     - `data.records:read`
     - `data.records:write`
     - `schema.bases:read`
4. Save the application and note down:
   - Client ID
   - Client Secret (if available)

### 2. Environment Setup
1. Create a `.env` file in the project root:
```env
AIRTABLE_CLIENT_ID=your_client_id
AIRTABLE_CLIENT_SECRET=your_client_secret
FASTAPI_SECRET_KEY=your_secret_key  # Generate using: python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### 3. Initial Authentication
1. Run the token acquisition script:
```bash
python get_tokens.py
```

2. This will:
   - Open your browser
   - Ask you to log into Airtable
   - Request permission to access your bases
   - Save the tokens to `airtable_tokens.json`

### 4. Using the Agent

1. Basic usage:
```python
from agent_auth import AirtableAgent

# Create an agent instance
agent = AirtableAgent("customer-name")

# List all bases
bases = agent.list_bases()

# Get base ID by name
base_id = get_base_id_by_name(bases, "Base Name")

# List leads in a base
leads = agent.list_leads(base_id)

# Add a new lead
new_lead = agent.add_lead(base_id, {
    "Name": "John Doe",
    "Email": "john@example.com",
    "Phone": "123-456-7890",
    "Status": "New"
})
```

2. Run the example script:
```bash
python use_agent.py
```

## Token Management

- Access tokens expire after 1-2 hours
- Refresh tokens expire after 60 days
- The agent automatically handles token refresh
- Tokens are stored in:
  - `airtable_tokens.json`: Raw tokens from Airtable
  - `agent_credentials_{agent_id}.json`: Agent's persistent storage

## Security Considerations

1. **Token Storage**:
   - Keep token files secure
   - Don't commit them to version control
   - Consider encrypting sensitive data

2. **Environment Variables**:
   - Keep `.env` file secure
   - Don't commit it to version control
   - Use different credentials for development and production

3. **Access Control**:
   - Monitor agent usage
   - Regularly audit permissions
   - Revoke access if needed through Airtable settings

## Deployment Steps

1. **Prepare Environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Application**:
   - Update `.env` with production credentials
   - Set appropriate redirect URI in Airtable OAuth settings
   - Generate new secret key for production

3. **Initial Setup**:
   - Run `get_tokens.py` once to obtain tokens
   - Save tokens securely
   - Create agent instances for each customer

4. **Regular Maintenance**:
   - Monitor token expiration
   - Backup token files
   - Update dependencies regularly

## Troubleshooting

1. **Authentication Errors**:
   - Check if tokens are expired
   - Verify OAuth credentials
   - Ensure correct redirect URI

2. **API Errors**:
   - Check base ID and table names
   - Verify required fields
   - Check permission levels

3. **Token Refresh Issues**:
   - Verify refresh token is valid
   - Check if refresh token is expired
   - Re-authenticate if needed

## Support

For issues or questions:
1. Check the [Airtable API Documentation](https://airtable.com/developers/web/api/introduction)
2. Review error messages in logs
3. Contact Airtable support for API-related issues

## License

This project is licensed under the MIT License - see the LICENSE file for details.