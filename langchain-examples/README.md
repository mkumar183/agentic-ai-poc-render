## local server runs on 61495 on vercel localhost and then fastapi runs on 8000
result can be stored in supabase for review later 
moving to spam should be done rule based rather than calling openai 
keep adding users to supabase to keep reducing spams 

## to run the fastAPI 
source venv/bin/activate && export $(cat .env | xargs) && python email-assistant.py

## to call the API
curl -X POST http://localhost:8000/process-emails

## refresh token 
rm -f token.pickle 