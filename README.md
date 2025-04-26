# agentic-ai-poc-render
agentic ai poc deployed using render


# create virtual env 
python3 -m venv venv 

# activate vend && build 
source venv/bin/activate && pip3 install -r requirements.txt

# start fastapi server
uvicorn main:app --reload 

# install playwright 
pip3 install playwright # part of requirements.txt

# downloads browser binaries (Chromium, Firefox, WebKit) locally.
playwright install 