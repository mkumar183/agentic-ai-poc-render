import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

load_dotenv()

# --- Configuration ---
# Replace with your actual bot token obtained from @BotFather
# get it from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Replace with your actual chat ID obtained from @userinfobot
# It can be a positive number for a user, or a negative number for a group.
CHAT_ID = os.getenv("CHAT_ID")

# Initialize FastAPI app
app = FastAPI()

def get_spiritual_quote():
    """
    Fetches the daily quote from spiritualdiary.org's JSON file
    Returns a tuple of (date, topic, quote, author, source)
    """
    try:
        # Fetch the JSON file
        response = requests.get('http://spiritualdiary.org/assets/json/sd.json')
        response.raise_for_status()
        
        # Parse the JSON data
        data = response.json()
        
        # Get current month and day
        current_date = datetime.now()
        current_month = f"m_{current_date.month}"
        current_day = f"d_{current_date.day}"
        
        # Get today's quote from the nested structure
        if current_month in data and current_day in data[current_month]:
            quote_data = data[current_month][current_day]
            date = f"{current_date.strftime('%B')} {current_date.day}"
            topic = quote_data.get('topic', '')
            quote = quote_data.get('quote', '')
            author = quote_data.get('author', '')
            source = quote_data.get('source', '')
            
            return date, topic, quote, author, source
        else:
            print(f"No quote found for {current_month} {current_day}")
            return None
            
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return None

def format_quote_message(date, topic, quote, author, source):
    """Formats the quote components into a nice message"""
    return f"""📅 Date: {date} 📌 Topic: {topic}

💭 {quote}

✍️ {author}
📚 {source}"""

# --- Function to send a message ---
async def send_telegram_message(message_text: str):
    """
    Sends a simple text message to the specified Telegram chat.

    Args:
        message_text (str): The text content of the message to send.
    """
    try:
        # Initialize the Bot object with your token
        bot = Bot(token=BOT_TOKEN)

        # Send the message
        await bot.send_message(chat_id=CHAT_ID, text=message_text)
        print(f"Message successfully sent to chat ID {CHAT_ID}: '{message_text}'")
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

@app.get("/api/telegram-connector")
async def send_quote():
    """API endpoint to send the daily quote"""
    try:
        # Get the spiritual quote
        quote_data = get_spiritual_quote()
        
        if quote_data:
            date, topic, quote, author, source = quote_data
            formatted_message = format_quote_message(date, topic, quote, author, source)
            
            # Send the formatted quote
            success = await send_telegram_message(formatted_message)
            
            if success:
                return JSONResponse(
                    status_code=200,
                    content={
                        'status': 'success',
                        'message': 'Quote sent successfully'
                    }
                )
            else:
                raise HTTPException(status_code=500, detail="Failed to send message")
        else:
            raise HTTPException(status_code=404, detail="No quote found for today")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)