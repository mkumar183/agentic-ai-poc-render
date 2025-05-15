from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio, os

from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.environ.get("GEMINI_API_KEY")

model_client = OpenAIChatCompletionClient(
    model="gemini-1.5-flash-8b",
    api_key=gemini_api_key,
)

response = asyncio.run(model_client.create([UserMessage(content="What is the capital of France?", source="user")]))
print(response.content)
# asyncio.run(model_client.close())