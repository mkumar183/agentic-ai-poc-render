import os
import asyncio
from autogen_core.models import UserMessage
from autogen_ext.models.azure import AzureAIChatCompletionClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()
github_token = os.environ.get("GITHUB_TOKEN")


client = AzureAIChatCompletionClient(
    model="Phi-4",
    endpoint="https://models.inference.ai.azure.com",
    # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
    # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
    credential=AzureKeyCredential(github_token),
    model_info={
        "json_output": False,
        "function_calling": False,
        "vision": False,
        "family": "unknown",
        "structured_output": False,
    },
)

result = asyncio.run(client.create([UserMessage(content="What is the capital of France?", source="user")]))
print(result)
# await client.close()

asyncio.run(client.close())
