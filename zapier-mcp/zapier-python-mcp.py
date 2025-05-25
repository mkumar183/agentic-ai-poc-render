import asyncio
import json
import os
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

load_dotenv()

# Create the transport with your MCP server URL
server_url = os.getenv("MCP_SERVER_URL")
transport = StreamableHttpTransport(server_url)

# Initialize the client with the transport
client = Client(transport=transport)


async def create_google_calendar_event(client):
    print("Calling google_calendar_create_detailed_event...")
    result = await client.call_tool(
        "google_calendar_create_detailed_event",
        {
            "instructions": "Execute the Google Calendar: Create Detailed Event tool with the following parameters",
            "calendarid": "mkumar183@gmail.com",
            "summary": "Test Event Tushar",
            "description": "This is a test event from zapier-mcp tushar",
            "start__dateTime": "2025-05-25T07:05:26.117Z",
            "end__dateTime": "2025-05-25T07:05:26.117Z",
        },
    )
    json_result = json.loads(result[0].text)
    print(f"\ngoogle_calendar_create_detailed_event result:\n{json.dumps(json_result, indent=2)}")
    return result


async def send_slack_message(client):
    print("Calling slack_send_channel_message...")
    result = await client.call_tool(
        "slack_send_channel_message",
        {
            "instructions": "Execute the Slack: Send Channel Message tool with the following parameters",
            "text": "This is a test message from zapier-mcp tushar",
            "channel": "nuragi-lab",
        },
    )
    json_result = json.loads(result[0].text)
    print(f"\nslack_send_channel_message result:\n{json.dumps(json_result, indent=2)}")
    return result


async def send_telegram_message(client):
    print("Calling telegram_send_message...")
    # get chatid from env file
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    result = await client.call_tool(
        "telegram_send_message",
        {
            "instructions": "Execute the Telegram: Send Message tool with the following parameters",
            "text": "This is a test message from zapier-mcp manoj",
            "chat_id": chat_id,
        },
    )
    json_result = json.loads(result[0].text)
    print(f"\ntelegram_send_message result:\n{json.dumps(json_result, indent=2)}")
    return result


async def main():
    # Connection is established here
    print("Connecting to MCP server...")
    async with client:
        print(f"Client connected: {client.is_connected()}")

        # Make MCP calls within the context
        print("Fetching available tools...")
        tools = await client.list_tools()
        print(f"Available tools: {json.dumps([t.name for t in tools], indent=2)}")

        # Uncomment the method you want to test
        # await create_google_calendar_event(client)
        # await send_slack_message(client)
        await send_telegram_message(client)

    # Connection is closed automatically when exiting the context manager
    print("Example completed")


if __name__ == "__main__":
    asyncio.run(main())
