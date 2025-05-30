# to run from scratch:
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

to run server
uvicorn api:app --reload