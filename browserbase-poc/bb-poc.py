from browserbase import Browserbase
import os
from dotenv import load_dotenv
import time

def login_to_linkedin():
    print("\n=== Starting LinkedIn Login Process ===")
    
    # Load environment variables
    print("\nStep 1: Loading environment variables...")
    load_dotenv()
    LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    BROWSERBASE_API_KEY = os.getenv("BROWSERBASE_API_KEY")
    
    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        print("❌ Error: Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in your .env file")
        return
        
    if not BROWSERBASE_API_KEY:
        print("❌ Error: Please set BROWSERBASE_API_KEY in your .env file")
        return

    print("✅ Environment variables loaded successfully")
    
    # Initialize BrowserBase
    print("\nStep 2: Initializing BrowserBase...")
    browser = Browserbase(api_key=BROWSERBASE_API_KEY)
    print("✅ BrowserBase initialized")
    
    try:
        # Navigate to LinkedIn
        print("\nStep 3: Navigating to LinkedIn login page...")
        browser.get("https://www.linkedin.com/login")
        print("✅ Successfully reached LinkedIn login page")
        
        # Fill in login form
        print("\nStep 4: Filling login credentials...")
        print("   - Entering email...")
        browser.type("#username", LINKEDIN_EMAIL)
        print("   - Entering password...")
        browser.type("#password", LINKEDIN_PASSWORD)
        print("   - Clicking login button...")
        browser.click("button[type='submit']")
        print("✅ Login form submitted")
        
        # Wait for login to complete
        print("\nStep 5: Waiting for login to complete...")
        browser.wait_for_element(".global-nav", timeout=60000)
        print("✅ Login successful!")
        
        # Handle security verification if needed
        if browser.element_exists("text=Verify you're not a robot"):
            print("\n⚠️ Security verification required!")
            print("Please complete the verification in the browser window...")
            browser.wait_for_element(".global-nav", timeout=120000)
            print("✅ Security verification completed")
        
        # Extract information from home page
        print("\nStep 6: Extracting information from home page...")
        
        # Get page title
        title = browser.get_title()
        print(f"   - Page Title: {title}")
        
        # Get current URL
        current_url = browser.get_url()
        print(f"   - Current URL: {current_url}")
        
        # Get feed posts
        print("\nStep 7: Extracting feed posts...")
        posts = browser.find_elements(".feed-shared-update-v2")
        print(f"   - Found {len(posts)} posts in feed")
        
        # Extract post information
        post_data = []
        for post in posts[:5]:  # Get first 5 posts
            try:
                author = post.find_element(".feed-shared-actor__name").get_text()
                content = post.find_element(".feed-shared-text").get_text()
                post_data.append({
                    'author': author,
                    'content': content[:200] + '...' if len(content) > 200 else content
                })
            except Exception as e:
                print(f"   - Error extracting post: {str(e)}")
        
        # Print post information
        print("\nRecent Posts:")
        for i, post in enumerate(post_data, 1):
            print(f"\nPost {i}:")
            print(f"Author: {post['author']}")
            print(f"Content: {post['content']}")
        
        print("\n=== Login and Data Extraction Completed Successfully ===")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
    
    finally:
        print("\nClosing browser...")
        browser.close()
        print("✅ Browser closed")

if __name__ == "__main__":
    print("=== LinkedIn BrowserBase Script Started ===")
    login_to_linkedin()
    print("=== Script Execution Completed ===")
