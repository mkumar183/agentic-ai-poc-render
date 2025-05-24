from utils import init_arcade_client
import json


client = init_arcade_client()


USER_ID = "manoj@nuragi.com"
TOOL_NAME = "Search.SearchGoogle"

# Define three different search queries
search_queries = {
    "AI Startups and Funding": "AI startups funding news OR new AI companies launched",
    "AI Platform Updates": "AI platform updates OR new AI features OR AI tool enhancements",
    "AI Implementation": "companies implementing AI technology OR AI adoption news"
}

# Perform and display results for each search
for category, query in search_queries.items():
    tool_input = {"query": query, "n_results": 5}
    
    response = client.tools.execute(
        tool_name=TOOL_NAME,
        input=tool_input,
        user_id=USER_ID,
    )
    
    news_items = json.loads(response.output.value)
    
    print(f"\n=== {category} ===\n")
    
    for item in news_items:
        print(f"Title: {item['title']}")
        print(f"Source: {item['source']}")
        print(f"Link: {item['link']}")
        if 'snippet' in item:
            print(f"Summary: {item['snippet']}")
        print("\n" + "-"*80 + "\n")
