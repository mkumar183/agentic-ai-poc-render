from arcadepy import Arcade
from utils import init_arcade_client


# import os 
# from dotenv import load_dotenv

# load_dotenv()
# arcade_api_key = os.getenv("ARCADE_API_KEY")
# client = Arcade(api_key=arcade_api_key)  # Initialize with explicit API key

client = init_arcade_client()

USER_ID = "manoj@nuragi.com"
TOOL_NAME = "Slack.SendMessageToChannel"

auth_response = client.tools.authorize(
    tool_name=TOOL_NAME,
    user_id=USER_ID,
)

if auth_response.status != "completed":
    print(f"Click this link to authorize: {auth_response.url}")

# Wait for the authorization to complete
client.auth.wait_for_completion(auth_response)

tool_input = {"channel_name": "nuragi-lab", "message": "Hello, this message is using arcade bot!"}

response = client.tools.execute(
    tool_name=TOOL_NAME,
    input=tool_input,
    user_id=USER_ID,
)
print(response)
