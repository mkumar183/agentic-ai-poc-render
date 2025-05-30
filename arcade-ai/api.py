from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add the current directory to Python path to import the module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from google_search import search_and_send_news

app = FastAPI(title="AI News Search API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchResponse(BaseModel):
    message: str
    status: str

@app.get("/")
async def root():
    return {"message": "AI News Search API is running"}

@app.post("/search-news", response_model=SearchResponse)
async def search_news():
    print("Searching for news...")
    try:
        search_and_send_news()
        return SearchResponse(
            message="News search completed and sent to Slack",
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 