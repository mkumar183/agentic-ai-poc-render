from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import ToolCallSummaryMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import asyncio
import os
import math

load_dotenv()

# Define web search tool
async def web_search_func(query: str) -> str:
    """Find information on the web"""
    return "AutoGen is a programming framework for building multi-agent applications 123."

# Define factorial tool
async def factorial_func(n: int) -> str:
    """Calculate the factorial of a number"""
    if n < 0:
        return "Factorial is not defined for negative numbers"
    try:
        result = math.factorial(n)
        return f"The factorial of {n} is {result}"
    except Exception as e:
        return f"Error calculating factorial: {str(e)}"

# Create function tools
web_search_function_tool = FunctionTool(
    web_search_func, 
    description="Find information on the web. Use this when you need to search for general information or facts."
)

factorial_function_tool = FunctionTool(
    factorial_func,
    description="Calculate the factorial of a number. Use this when you need to compute factorial of a non-negative integer."
)

# Create an agent that uses the OpenAI model
model_client = OpenAIChatCompletionClient(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY"),
)

agent = AssistantAgent(
    name="multi_tool_assistant",
    model_client=model_client,
    tools=[web_search_function_tool, factorial_function_tool],
    system_message="""You are a helpful assistant that can use different tools based on the task:
    - Use web search for finding information and facts
    - Use factorial calculator for mathematical calculations
    Choose the appropriate tool based on the user's request.""",
)

async def main():
    # Test cases to demonstrate tool selection
    test_tasks = [
        "What is AutoGen?",
        "Calculate factorial of 5",
        "What is the factorial of 7?",
        "Tell me about Python programming language"
    ]
    
    for task in test_tasks:
        print(f"\nTask: {task}")
        result = await agent.run(task=task)
        
        # Print the tool call results
        for message in result.messages:
            if isinstance(message, ToolCallSummaryMessage):
                print(f"Result: {message.content}")

# Run the async main function
asyncio.run(main())
