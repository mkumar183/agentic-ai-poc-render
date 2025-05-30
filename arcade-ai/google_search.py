from utils import init_arcade_client
import json
from datetime import datetime, timedelta
from slack_channel import send_slack_message
import os
from dotenv import load_dotenv
load_dotenv()
# get channel name from env
channel_name = os.getenv("SLACK_CHANNEL")


def format_news_message(category: str, news_items: list) -> str:
    """Format news items into a readable message for Slack."""
    message = f"📰 *{category.upper()}*\n"
    message += "=" * 50 + "\n\n"
    
    for item in news_items:
        title = item['title'].replace(' - ', ': ').split('|')[0].strip()
        message += f"🔹 *{title}*\n"
        message += f"🔗 {item['link']}\n"
        
        if 'snippet' in item and len(item['snippet']) > 20:
            message += f"📝 {item['snippet'][:200]}...\n"
        
        message += "-" * 50 + "\n\n"
    
    return message

def search_and_send_news(user_id: str = "agent-veridian@nuragi.com"):
    """Search for AI news and send results to Slack."""
    client = init_arcade_client()
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

    for category, query in search_queries.items():
        tool_input = {
            "query": query,
            "n_results": 3,
            "sort_by": "date"
        }
        
        try:
            response = client.tools.execute(
                tool_name=TOOL_NAME,
                input=tool_input,
                user_id=user_id,
            )
            
            news_items = json.loads(response.output.value)
            
            # Print to console
            print(f"\n📰 {category.upper()}")
            print("=" * 50)
            
            for item in news_items:
                title = item['title'].replace(' - ', ': ').split('|')[0].strip()
                print(f"\n🔹 {title}")
                print(f"🔗 {item['link']}")
                if 'snippet' in item and len(item['snippet']) > 20:
                    print(f"📝 {item['snippet'][:200]}...")
                print("-" * 50)
            
            # Send to Slack
            slack_message = format_news_message(category, news_items)            
            send_slack_message(channel_name, slack_message, user_id)
                
        except Exception as e:
            error_message = f"Error fetching {category}: {str(e)}"
            print(error_message)
            send_slack_message("ai-news", f"❌ {error_message}", user_id)
            continue

    print("\n=== End of News Feed ===\n")

if __name__ == "__main__":
    search_and_send_news() 