from playwright.sync_api import sync_playwright, TimeoutError
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time

def save_jobs_to_json(jobs, filename="linkedin_jobs.json"):
    """Save jobs data to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(jobs, f, indent=2)

def load_jobs_from_json(filename="linkedin_jobs.json"):
    """Load previously saved jobs from JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def is_job_recent(posted_date):
    """Check if job was posted within the last 24 hours"""
    if "hour" in posted_date.lower() or "minute" in posted_date.lower():
        return True
    if "day" in posted_date.lower():
        days = int(''.join(filter(str.isdigit, posted_date)))
        return days <= 1
    return False

def main():
    # Load environment variables
    load_dotenv()
    LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    
    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in your .env file")
        return

    # Load previously saved jobs
    previous_jobs = load_jobs_from_json()
    previous_job_ids = {job['id'] for job in previous_jobs}

    browser = None
    try:
        with sync_playwright() as p:
            # Launch browser with additional options for stability
            print("Launching browser...")
            browser = p.chromium.launch(
                headless=False,  # Set to True in production
                args=[
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-software-rasterizer'
                ]
            )
            
            # Create a new context with viewport size
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            )
            
            # Enable request interception for better performance
            page = context.new_page()
            
            try:
                # Navigate to LinkedIn with retry logic
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        print(f"Navigating to LinkedIn (attempt {attempt + 1}/{max_retries})...")
                        page.goto("https://www.linkedin.com/login", timeout=60000)
                        break
                    except TimeoutError:
                        if attempt == max_retries - 1:
                            raise
                        print("Timeout occurred, retrying...")
                        time.sleep(5)
                
                # Login with retry logic
                print("Logging in...")
                page.fill("#username", LINKEDIN_EMAIL)
                page.fill("#password", LINKEDIN_PASSWORD)
                page.click("button[type='submit']")
                
                # Wait for login to complete with increased timeout
                page.wait_for_selector(".global-nav", timeout=60000)
                print("Successfully logged in!")

                # Navigate to jobs with retry logic
                print("Navigating to jobs page...")
                page.goto("https://www.linkedin.com/jobs/", timeout=60000)
                page.wait_for_selector(".jobs-search-box", timeout=60000)

                # Search for jobs (you can customize these parameters)
                search_keywords = "software engineer"  # Customize this
                location = "United States"  # Customize this
                
                # Fill in search form with retry logic
                page.fill(".jobs-search-box__text-input[aria-label*='Search job titles']", search_keywords)
                page.fill(".jobs-search-box__text-input[aria-label*='City, state, or zip code']", location)
                page.click(".jobs-search-box__submit-button")
                
                # Wait for results with increased timeout
                page.wait_for_selector(".jobs-search-results__list", timeout=60000)
                
                # Filter for recent jobs
                print("Filtering for recent jobs...")
                page.click("button[aria-label*='Date posted filter']")
                page.click("text=Past 24 hours")
                page.wait_for_selector(".jobs-search-results__list", timeout=60000)

                # Extract job information
                jobs = []
                job_cards = page.query_selector_all(".jobs-search-results__list-item")
                
                for card in job_cards:
                    try:
                        job_id = card.get_attribute("data-job-id")
                        if job_id in previous_job_ids:
                            continue

                        title = card.query_selector(".job-card-list__title").inner_text()
                        company = card.query_selector(".job-card-container__company-name").inner_text()
                        location = card.query_selector(".job-card-container__metadata-item").inner_text()
                        posted_date = card.query_selector(".job-card-container__footer-item").inner_text()
                        
                        # Get job details with retry logic
                        max_retries = 3
                        for attempt in range(max_retries):
                            try:
                                card.click()
                                page.wait_for_selector(".jobs-description", timeout=10000)
                                description = page.query_selector(".jobs-description").inner_text()
                                break
                            except TimeoutError:
                                if attempt == max_retries - 1:
                                    raise
                                print(f"Timeout getting job details, retrying... (attempt {attempt + 1})")
                                time.sleep(2)
                        
                        job_data = {
                            "id": job_id,
                            "title": title,
                            "company": company,
                            "location": location,
                            "posted_date": posted_date,
                            "description": description,
                            "found_date": datetime.now().isoformat()
                        }
                        
                        jobs.append(job_data)
                        print(f"Found new job: {title} at {company}")
                        
                    except Exception as e:
                        print(f"Error processing job card: {str(e)}")
                        continue

                # Save all jobs (previous + new)
                all_jobs = previous_jobs + jobs
                save_jobs_to_json(all_jobs)
                
                print(f"\nFound {len(jobs)} new jobs!")
                print(f"Total jobs saved: {len(all_jobs)}")

            except Exception as e:
                print(f"An error occurred during page operations: {str(e)}")
                # Take error screenshot
                try:
                    page.screenshot(path="linkedin_error.png")
                    print("Error screenshot saved as linkedin_error.png")
                except:
                    print("Could not save error screenshot")
            finally:
                # Take a screenshot before closing
                try:
                    page.screenshot(path="linkedin_jobs_page.png")
                except:
                    print("Could not save final screenshot")
                
                # Close context and browser
                try:
                    context.close()
                except:
                    print("Could not close context")
                
                try:
                    browser.close()
                except:
                    print("Could not close browser")

    except Exception as e:
        print(f"Critical error occurred: {str(e)}")
        if browser:
            try:
                browser.close()
            except:
                print("Could not close browser after critical error")

if __name__ == "__main__":
    main() 