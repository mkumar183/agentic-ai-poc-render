from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def is_api_call(url):
    # Filter out static assets and common non-API URLs
    non_api_extensions = ['.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf']
    non_api_paths = ['/favicon.ico', '/static/', '/assets/', '/images/']
    
    # Check if URL ends with any non-API extension
    if any(url.endswith(ext) for ext in non_api_extensions):
        return False
    
    # Check if URL contains any non-API paths
    if any(path in url for path in non_api_paths):
        return False
    
    # Check if it's a REST API call (contains /api/ or ends with common API patterns)
    api_patterns = ['/api/', '/auth/', '/graphql', '/rest/', '/v1/', '/v2/']
    return any(pattern in url for pattern in api_patterns)

def run(playwright):
    browser = playwright.chromium.launch(headless=True)  # Headless browser
    page = browser.new_page()
    
    # Set up request interception
    jwt_token = None
    api_calls = []
    
    def handle_request(request):
        if is_api_call(request.url):
            # Log the request
            api_calls.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'REQUEST',
                'method': request.method,
                'url': request.url,
                'headers': request.headers
            })
    
    def handle_response(response):
        nonlocal jwt_token
        if is_api_call(response.url):
            # Log the response
            api_calls.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'RESPONSE',
                'method': response.request.method,
                'url': response.url,
                'status': response.status,
                'headers': response.headers
            })
            
        # Process Supabase auth response
        if "supabase.co/auth/v1/token" in response.url and jwt_token is None:
            try:
                data = response.json()
                if 'access_token' in data:
                    jwt_token = data['access_token']
                    print("\n=== JWT Token Captured ===")
                    print(f"Token: {jwt_token}")
                    print("=== Token Details ===")
                    print(f"Token Type: {data.get('token_type')}")
                    print(f"Expires In: {data.get('expires_in')} seconds")
                    print(f"Expires At: {data.get('expires_at')}")
                    print("====================\n")
            except Exception as e:
                print(f"Error processing auth response: {e}")
    
    # Listen for requests and responses
    page.on("request", handle_request)
    page.on("response", handle_response)
    
    # Navigate to login page
    page.goto("http://localhost:8080/")
    
    # Fill in login form
    page.fill('input[name="email"]', 'sachdeva@maxfort.edu')
    page.fill('input[name="password"]', 'password')
    page.click('button[type="submit"]')
    
    # Wait for navigation to complete
    page.wait_for_load_state('networkidle')
    
    print("\nPage title:", page.title())
    
    # Take screenshot
    page.screenshot(path="logged_in_page.png")
    print("Screenshot saved as logged_in_page.png")
    
    # Print all API calls
    print("\n=== REST API Calls Log ===")
    for call in api_calls:
        # print(f"\n{call['timestamp']} - {call['type']}")
        # print(f"Method: {call['method']}")
        print(f"URL: {call['url']}")
        # if call['type'] == 'RESPONSE':
        #     print(f"Status: {call['status']}")
        # print("---")
    
    # Save API calls to a file
    with open('api_calls.json', 'w') as f:
        json.dump(api_calls, f, indent=2)
    print("\nAPI calls saved to api_calls.json")
    
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
