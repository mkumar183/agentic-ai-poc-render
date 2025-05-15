from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

print("Starting script...")
load_dotenv()
print("Environment variables loaded")

async def scrape_webpage(url: str) -> str:
    """Scrape content from a webpage"""
    try:
        print(f"Fetching content from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])
        
        print("Content fetched successfully")
        return content
    except Exception as e:
        print(f"Error fetching content: {str(e)}")
        return f"Error: Could not fetch content from {url}"

async def main():
    print("\n=== Starting main function ===")
    
    try:
        print("\nInitializing OpenAI client...")
        model_client = OpenAIChatCompletionClient(
            model="gpt-4.1-nano",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        print("OpenAI client initialized")
        
        print("\nCreating assistant agent...")
        assistant = AssistantAgent(
            name="web_assistant",
            model_client=model_client,
            system_message="You are a helpful assistant that summarizes web content."
        )
        print("Assistant agent created")

        # Example URL
        url = "https://en.wikipedia.org/wiki/Seattle"
        
        print("\nScraping webpage...")
        content = await scrape_webpage(url)
        
        if content.startswith("Error"):
            print(content)
            return
            
        print("\nGenerating summary...")
        result = await assistant.run(
            task=f"Please summarize the following content in 3-4 sentences:\n\n{content[:2000]}"  # Limiting content length
        )
        
        if isinstance(result.messages[-1], TextMessage):
            print("\n=== Summary ===")
            print(result.messages[-1].content)
            print("=== End Summary ===")
        else:
            print("Unexpected message type received")
            print(f"Message type: {type(result.messages[-1])}")

        print("\nClosing model client...")
        await model_client.close()
        print("Model client closed")
            
    except Exception as e:
        print(f"\nERROR: An error occurred: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
    finally:
        print("\n=== Cleanup completed ===")

if __name__ == "__main__":
    print("\n=== Script execution started ===")
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\nCRITICAL ERROR: Failed to run main function: {str(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
    print("\n=== Script execution completed ===") 