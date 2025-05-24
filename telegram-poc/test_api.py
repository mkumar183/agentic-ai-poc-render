import requests

def test_telegram_api():
    # Replace with your actual Vercel deployment URL
    url = "https://your-vercel-domain.vercel.app/api/telegram-connector"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == "__main__":
    test_telegram_api() 