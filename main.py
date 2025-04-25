from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Optional
from datetime import datetime

from database import supabase

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI configuration
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
async def read_root():
    return {"message": "Welcome to AI Tutor API!"}

@app.post("/conversations")
async def create_conversation():
    try:
        # Create a new conversation in Supabase
        conversation = supabase.table("conversations").insert({
            "title": "New Conversation",
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        
        return conversation.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations")
async def get_conversations():
    try:
        conversations = supabase.table("conversations").select("*").execute()
        return conversations.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: int):
    try:
        conversation = supabase.table("conversations").select("*").eq("id", conversation_id).execute()
        if not conversation.data:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations/{conversation_id}/messages")
async def get_messages(conversation_id: int):
    try:
        messages = supabase.table("messages").select("*").eq("conversation_id", conversation_id).execute()
        return messages.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/conversations/{conversation_id}/messages")
async def create_message(conversation_id: int, request: Request):
    try:
        # Get user message from request
        data = await request.json()
        user_message = data.get("message")
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Save user message to Supabase
        user_msg = supabase.table("messages").insert({
            "conversation_id": conversation_id,
            "role": "user",
            "content": user_message,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        
        # Get conversation history
        messages = supabase.table("messages").select("*").eq("conversation_id", conversation_id).execute()
        conversation_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages.data
        ]
        
        # Get AI response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history + [{"role": "user", "content": user_message}]
        )
        ai_response = response.choices[0].message.content
        
        # Save AI response to Supabase
        ai_msg = supabase.table("messages").insert({
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": ai_response,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        
        return {
            "user_message": user_message,
            "ai_response": ai_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
