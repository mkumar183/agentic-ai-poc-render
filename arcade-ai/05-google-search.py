from utils import init_arcade_client
import json
from datetime import datetime, timedelta

client = init_arcade_client()

USER_ID = "manoj@nuragi.com"
TOOL_NAME = "Search.SearchGoogle"

# Get yesterday's date for filtering
yesterday = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# Define focused search queries for recent AI news
search_queries = {
    "AI Breakthroughs": f"AI breakthrough OR AI innovation OR AI advancement after:{yesterday}",
    "AI Funding": f"AI startup funding OR AI company raised OR AI investment after:{yesterday}",
    "AI Success Stories": f"AI success story OR AI implementation success OR AI transformation after:{yesterday}",
    "AI Product Launches": f"new AI product launch OR new AI tool release OR AI platform launch after:{yesterday}"
}

print(f"\n=== Latest AI News (Since {yesterday}) ===\n")

# Perform and display results for each search
for category, query in search_queries.items():
    tool_input = {
        "query": query,
        "n_results": 3,  # Reduced to get more focused results
        "sort_by": "date"  # Sort by date to get latest news first
    }
    
    try:
        response = client.tools.execute(
            tool_name=TOOL_NAME,
            input=tool_input,
            user_id=USER_ID,
        )
        
        news_items = json.loads(response.output.value)
        
        print(f"\n📰 {category.upper()}")
        print("=" * 50)
        
        for item in news_items:
            # Clean and format the title
            title = item['title'].replace(' - ', ': ').split('|')[0].strip()
            
            # Print formatted output
            print(f"\n🔹 {title}")
            print(f"🔗 {item['link']}")
            
            # Print snippet if available and relevant
            if 'snippet' in item and len(item['snippet']) > 20:
                print(f"📝 {item['snippet'][:200]}...")
            
            print("-" * 50)
            
    except Exception as e:
        print(f"Error fetching {category}: {str(e)}")
        continue

print("\n=== End of News Feed ===\n")
