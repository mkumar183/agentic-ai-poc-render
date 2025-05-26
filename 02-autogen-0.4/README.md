# On Windows, change `python3` to `python` (if `python` is Python 3).
python3 -m venv .venv
# On Windows, change `bin` to `scripts`.
source .venv/bin/activate

pip install -U "autogen-agentchat"

pip install "autogen-ext[openai]"
If you are using Azure OpenAI with AAD authentication, you need to install the following:

pip install "autogen-ext[azure]"

# following:
https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/installation.html

pip freeze > requirements.txt