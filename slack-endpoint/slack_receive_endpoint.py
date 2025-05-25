from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Slack endpoint is running"}

@app.post("/slack/message")
async def receive_slack_message(request: Request):
    try:
        # Get the request body
        data = await request.json()
        
        # Handle URL verification challenge
        if data.get("type") == "url_verification":
            challenge = data.get("challenge")
            logger.info(f"Received URL verification challenge: {challenge}")
            return JSONResponse(content={"challenge": challenge})
        
        # Extract message details
        text = data.get("text", "")
        channel = data.get("channel", "")
        user = data.get("user", "")
        
        # Log the received message
        logger.info(f"Received message from {user} in channel {channel}: {text}")
        
        # Return a success response
        return JSONResponse(content={
            "status": "success",
            "message": "Message received"
        })
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 