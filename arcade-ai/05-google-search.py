from arcadepy import Arcade
from utils import init_arcade_client
import json


client = init_arcade_client()


USER_ID = "manoj@nuragi.com"
TOOL_NAME = "Search.SearchGoogle"

tool_input = {"query": "AI News this week?", "n_results": 10}

response = client.tools.execute(
    tool_name=TOOL_NAME,
    input=tool_input,
    user_id=USER_ID,
)

# Parse the response value as JSON
news_items = json.loads(response.output.value)

print("\n=== Latest AI News ===\n")

for item in news_items:
    print(f"Title: {item['title']}")
    print(f"Source: {item['source']}")
    print(f"Link: {item['link']}")
    if 'snippet' in item:
        print(f"Summary: {item['snippet']}")
    print("\n" + "-"*80 + "\n")
