from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import time

def run(playwright):
    print("\n=== Starting LinkedIn Login Process ===")
    
    # Load environment variables
    print("\nStep 1: Loading environment variables...")
    load_dotenv()
    LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    
    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        print("❌ Error: Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in your .env file")
        return

    print("✅ Environment variables loaded successfully")
    
    # Launch browser
    print("\nStep 2: Launching browser...")
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    print("✅ Browser launched successfully")
    
    try:
        # Navigate to LinkedIn
        print("\nStep 3: Navigating to LinkedIn login page...")
        page.goto("https://www.linkedin.com")
        print("✅ Successfully reached LinkedIn page")

        page.goto("https://www.linkedin.com/login")
        print("✅ Successfully reached LinkedIn login page")
        
        # Fill in login form
        print("\nStep 4: Filling login credentials...")
        print("   - Entering email...")
        page.fill("#username", LINKEDIN_EMAIL)
        print("   - Entering password...")
        page.fill("#password", LINKEDIN_PASSWORD)
        print("   - Clicking login button...")
        page.click("button[type='submit']")
        print("✅ Login form submitted")
        
        # Wait for login to complete
        print("\nStep 5: Waiting for login to complete...")
        page.wait_for_selector(".global-nav", timeout=60000)
        print("✅ Login successful!")
        
        # Handle security verification if needed
        if page.query_selector("text=Verify you're not a robot"):
            print("\n⚠️ Security verification required!")
            print("Please complete the verification in the browser window...")
            page.wait_for_selector(".global-nav", timeout=120000)
            print("✅ Security verification completed")
        
        # Print page information
        print("\nStep 6: Getting page information...")
        print(f"   - Page Title: {page.title()}")
        print(f"   - Current URL: {page.url}")
        
        # Take screenshot
        print("\nStep 7: Taking screenshot...")
        page.screenshot(path="linkedin_logged_in.png")
        print("✅ Screenshot saved as linkedin_logged_in.png")
        
        print("\n=== Login Process Completed Successfully ===")
        print("You can now interact with the browser window")
        print("Press Enter to close the browser...")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        page.screenshot(path="linkedin_error.png")
        print("Error screenshot saved as linkedin_error.png")
    
    finally:
        input()  # Wait for user input before closing
        print("\nClosing browser...")
        browser.close()
        print("✅ Browser closed")

if __name__ == "__main__":
    print("=== LinkedIn Login Script Started ===")
    with sync_playwright() as playwright:
        run(playwright)
    print("=== Script Execution Completed ===") 