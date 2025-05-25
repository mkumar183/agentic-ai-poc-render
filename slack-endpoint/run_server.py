import subprocess
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_ngrok():
    # Start ngrok in a separate process
    ngrok_process = subprocess.Popen(
        ["ngrok", "http", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for ngrok to start
    time.sleep(2)
    
    # Get the public URL
    try:
        import requests
        tunnels = requests.get("http://localhost:4040/api/tunnels").json()
        public_url = tunnels["tunnels"][0]["public_url"]
        print(f"\nYour public URL is: {public_url}")
        print("Use this URL in your Slack app configuration")
        return public_url
    except Exception as e:
        print(f"Error getting ngrok URL: {e}")
        return None

def run_fastapi():
    # Start FastAPI server
    import uvicorn
    uvicorn.run("slack_receive_endpoint:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    # Start ngrok
    public_url = run_ngrok()
    
    if public_url:
        # Start FastAPI server
        run_fastapi() 