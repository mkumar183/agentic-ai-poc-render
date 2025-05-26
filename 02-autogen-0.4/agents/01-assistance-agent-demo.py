from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage, TextMessage, ToolCallSummaryMessage
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

# Define a tool that searches the web for information.
# For simplicity, we will use a mock function here that returns a static string.
async def web_search(query: str) -> str:
    """Find information on the web"""
    return "AutoGen is a programming framework for building multi-agent applications."


# Create an agent that uses the OpenAI GPT-4o model.
model_client = OpenAIChatCompletionClient(
    model="gpt-4.1-nano",
    api_key=os.getenv("OPENAI_API_KEY"),
)
agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    tools=[web_search],
    system_message="Use tools to solve tasks.",
)

# Use asyncio.run(agent.run(...)) when running in a script.
result = asyncio.run(agent.run(task="Find information on AutoGen"))

# Print only the content from each message
for message in result.messages:
    # print(f"Message: {message}")
    # type = ToolCallSummaryMessage print the content of the message
    if isinstance(message, ToolCallSummaryMessage):
        print(f"ToolCallSummaryMessage: {message.content}")


### example of multi modal message
from io import BytesIO
import PIL
import requests
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import Image

# Create a multi-modal message with random image and text.
pil_image = PIL.Image.open(BytesIO(requests.get("https://picsum.photos/300/200").content))
img = Image(pil_image)
multi_modal_message = MultiModalMessage(content=["Can you describe the content of this image?", img], source="user")

# # Save the image to a file
# output_path = "agents/random_image.jpg"
# pil_image.save(output_path)
# print(f"Image saved to: {output_path}")

# Display the image if running in interactive environment
try:
    pil_image.show()  # This will open the image in default image viewer
except Exception as e:
    print(f"Could not display image: {e}")

# Use asyncio.run(...) when running in a script.
result = asyncio.run(agent.run(task=multi_modal_message))
print(result.messages[-1].content)  # type: ignore

### example of streaming message

async def assistant_run_stream() -> None:
    # Option 1: read each message from the stream (as shown in the previous example).
    # async for message in agent.run_stream(task="Find information on AutoGen"):
    #     print(message)

    # Option 2: use Console to print all messages as they appear.
    await Console(
        agent.run_stream(task="Find information on AutoGen"),
        output_stats=True,  # Enable stats printing.
    )

# Use asyncio.run(assistant_run_stream()) when running in a script.
asyncio.run(assistant_run_stream())