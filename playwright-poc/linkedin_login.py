from playwright.sync_api import sync_playwright, TimeoutError, Error as PlaywrightError
import os
from dotenv import load_dotenv
import time
import sys

def create_browser_context(playwright, headless=False):
    """Create a new browser context with proper configuration"""
    try:
        browser = playwright.chromium.launch(
            headless=headless
            # args=[
            #     '--no-sandbox',
            #     '--disable-setuid-sandbox',
            #     '--disable-dev-shm-usage',
            #     '--disable-accelerated-2d-canvas',
            #     '--disable-gpu',
            #     '--window-size=1920,1080',
            #     '--enable-chrome-browser-cloud-management'
            # ]
        )
        page = browser.new_page()
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            storage_state="linkedin_auth.json" if os.path.exists("linkedin_auth.json") else None
        )
        
        return browser, context
    except Exception as e:
        print(f"Error creating browser context: {str(e)}")
        return None, None

def login_linkedin(username, password, headless=False, max_retries=3):
    """
    Login to LinkedIn and return the page object if successful
    
    Args:
        username (str): LinkedIn email
        password (str): LinkedIn password
        headless (bool): Whether to run browser in headless mode
        max_retries (int): Maximum number of retry attempts
    
    Returns:
        tuple: (success: bool, page: Page or None, browser: Browser or None)
    """
    browser = None
    page = None
    
    for attempt in range(max_retries):
        try:
            print(f"\nAttempt {attempt + 1} of {max_retries}")
            with sync_playwright() as p:
                # Create browser and context
                print("Creating browser context...")
                browser, context = create_browser_context(p, headless)
                if not browser or not context:
                    print("Failed to create browser context")
                    continue
                
                page = context.new_page()
                
                # Navigate to LinkedIn
                print("Navigating to LinkedIn...")
                page.goto("https://www.linkedin.com/login", timeout=60000)
                print(f"Current URL: {page.url}")
                
                # Check if already logged in
                if "feed" in page.url:
                    print("Already logged in!")
                    return True, page, browser
                
                # Login process
                print("Starting login process...")
                print("Filling username...")
                page.fill("#username", username)
                print("Filling password...")
                page.fill("#password", password)
                print("Clicking submit...")
                page.click("button[type='submit']")
                
                # Wait for login completion
                print("Waiting for login to complete...")
                try:
                    page.wait_for_selector(".global-nav", timeout=60000)
                    
                    # Handle security verification
                    if page.query_selector("text=Verify you're not a robot"):
                        print("Security verification required!")
                        print("Please complete the verification in the browser window...")
                        page.wait_for_selector(".global-nav", timeout=120000)
                    
                    # Save authentication state
                    context.storage_state(path="linkedin_auth.json")
                    print("Login successful!")
                    return True, page, browser
                    
                except TimeoutError:
                    error_message = page.query_selector(".alert-error")
                    if error_message:
                        print(f"Login failed: {error_message.inner_text()}")
                    else:
                        print("Login failed: Timeout waiting for navigation")
                        print(f"Current URL: {page.url}")
                    page.screenshot(path=f"login_failed_attempt_{attempt + 1}.png")
                    
                    # Don't retry if it's a credential error
                    if error_message and "password" in error_message.inner_text().lower():
                        return False, None, browser
                    
                    # Clean up for retry
                    try:
                        context.close()
                        browser.close()
                    except:
                        pass
                    continue
                
        except PlaywrightError as e:
            print(f"Playwright error: {str(e)}")
            if page:
                try:
                    page.screenshot(path=f"error_attempt_{attempt + 1}.png")
                    print(f"Error screenshot saved as error_attempt_{attempt + 1}.png")
                except:
                    pass
            continue
            
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            continue
            
        finally:
            if attempt < max_retries - 1:
                print("Waiting before retry...")
                time.sleep(5)
    
    print("All login attempts failed")
    return False, None, browser

def main():
    # Load environment variables
    load_dotenv()
    USERNAME = os.getenv("LINKEDIN_EMAIL")
    PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    
    if not USERNAME or not PASSWORD:
        print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in your .env file")
        return

    print(f"Attempting to login with email: {USERNAME}")
    success, page, browser = login_linkedin(USERNAME, PASSWORD)
    
    if success:
        print("Successfully logged in to LinkedIn!")
        print("You can now perform actions on the logged-in page")
        try:
            input("Press Enter to close the browser...")
        except KeyboardInterrupt:
            print("\nBrowser closing...")
    else:
        print("Failed to login to LinkedIn")
    
    # Clean up
    if browser:
        try:
            browser.close()
        except:
            print("Could not close browser")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)