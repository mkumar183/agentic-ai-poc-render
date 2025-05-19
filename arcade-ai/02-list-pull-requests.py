from arcadepy import Arcade

import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()



API_KEY = os.getenv("ARCADE_API_KEY")
USER_ID = "mkumar183"

client = Arcade(api_key=API_KEY)

# Authorize the tool
auth_response = client.tools.authorize(
    tool_name="Github.ListPullRequests@0.1.10",
    user_id=USER_ID,
)

# Check if authorization is completed
if auth_response.status != "completed":
    print(f"Click this link to authorize: {auth_response.url}")

# Wait for the authorization to complete
auth_response = client.auth.wait_for_completion(auth_response)

if auth_response.status != "completed":
    raise Exception("Authorization failed")

print("🚀 Authorization successful!")

result = client.tools.execute(
    tool_name="Github.ListPullRequests@0.1.10",
    input={
        "owner": "mkumar183",
        "name": "mkumar183",
        "starred": "true",
        "repo": "scholar-tenant-system"
    },
    user_id=USER_ID,
)

print(result)