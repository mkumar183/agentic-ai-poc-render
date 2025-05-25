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
        # logger.info(f"Received message: {data}")
        
        # Handle URL verification challenge
        if data.get("type") == "url_verification":
            challenge = data.get("challenge")
            logger.info(f"Received URL verification challenge: {challenge}")
            return JSONResponse(content={"challenge": challenge})
        
        # Handle event callback
        if data.get("type") == "event_callback":
            event = data.get("event", {})
            
            # Extract message details from the event
            text = event.get("text", "")
            channel = event.get("channel", "")
            user = event.get("user", "")
            channel_type = event.get("channel_type", "")
            ts = event.get("ts", "")
            
            # Log the received message
            logger.info(f"Received message from {user} in {channel_type} channel {channel} at {ts}: {text}")
            
            # Return a success response
            return JSONResponse(content={
                "status": "success",
                "message": "Message received"
            })
        
        # Return a default response for other events
        return JSONResponse(content={
            "status": "received",
            "message": "Event received but not processed"
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