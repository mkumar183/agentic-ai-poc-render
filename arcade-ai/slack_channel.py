from arcadepy import Arcade
from utils import init_arcade_client

def send_slack_message(channel_name: str, message: str, user_id: str = "agent-veridian@nuragi.com") -> None:
    """
    Send a message to a specified Slack channel using Arcade.
    
    Args:
        channel_name (str): Name of the Slack channel to send message to
        message (str): Message content to send
        user_id (str): User ID for authentication
    """
    client = init_arcade_client()
    TOOL_NAME = "Slack.SendMessageToChannel"

    # Get authorization
    auth_response = client.tools.authorize(
        tool_name=TOOL_NAME,
        user_id=user_id,
    )

    if auth_response.status != "completed":
        print(f"Click this link to authorize: {auth_response.url}")
        # Wait for user to complete authorization
        input("Press Enter after completing authorization...")

    tool_input = {"channel_name": channel_name, "message": message}

    response = client.tools.execute(
        tool_name=TOOL_NAME,
        input=tool_input,  # Changed back to 'input'
        user_id=user_id,
    )
    return response

if __name__ == "__main__":
    # Example usage
    response = send_slack_message("ai-news", "Hello, this message is using arcade bot!")
    print(response)
