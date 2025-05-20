from arcadepy import Arcade
from utils import init_arcade_client


client = init_arcade_client()  # Automatically finds the `ARCADE_API_KEY` env variable

USER_ID = "mkumar183@gmail.com"
TOOL_NAME = "Github.SetStarred"

auth_response = client.tools.authorize(
    tool_name=TOOL_NAME,
    user_id=USER_ID,
)

if auth_response.status != "completed":
    print(f"Click this link to authorize: {auth_response.url}")

# Wait for the authorization to complete
client.auth.wait_for_completion(auth_response)

tool_input = {"owner": "mkumar183", "name": "sqlparse", "starred": True}

response = client.tools.execute(
    tool_name=TOOL_NAME,
    input=tool_input,
    user_id=USER_ID,
)
print(response)
