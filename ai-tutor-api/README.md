# AI Tutor API

A FastAPI-based API for an AI tutoring system that uses OpenAI's GPT-3.5 and Supabase for data storage.

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## Running the API

Start the server with:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /`: Welcome message
- `POST /conversations`: Create a new conversation
- `GET /conversations`: List all conversations
- `GET /conversations/{conversation_id}`: Get a specific conversation
- `GET /conversations/{conversation_id}/messages`: Get messages in a conversation
- `POST /conversations/{conversation_id}/messages`: Add a new message to a conversation 