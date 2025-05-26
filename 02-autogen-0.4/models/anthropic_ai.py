import os, asyncio
from dotenv import load_dotenv

from autogen_core.models import UserMessage
from autogen_ext.models.semantic_kernel import SKChatCompletionAdapter
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.anthropic import AnthropicChatCompletion, AnthropicChatPromptExecutionSettings
from semantic_kernel.memory.null_memory import NullMemory

load_dotenv()
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")

sk_client = AnthropicChatCompletion(
    ai_model_id="claude-3-5-sonnet-20241022",
    api_key=anthropic_api_key,
    service_id="my-service-id",  # Optional; for targeting specific services within Semantic Kernel
)
settings = AnthropicChatPromptExecutionSettings(
    temperature=0.2,
)

anthropic_model_client = SKChatCompletionAdapter(
    sk_client, kernel=Kernel(memory=NullMemory()), prompt_settings=settings
)

# Call the model directly.
model_result = asyncio.run(anthropic_model_client.create(
    messages=[UserMessage(content="What is the capital of France?", source="User")]
))
print(model_result)
asyncio.run(anthropic_model_client.close())
