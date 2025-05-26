from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
import asyncio
import os
from dotenv import load_dotenv

print("Starting script...")
load_dotenv()
print("Environment variables loaded")

async def main():
    print("\n=== Starting main function ===")
    
    # Get the fetch tool from mcp-server-fetch
    print("Initializing MCP server parameters...")
    fetch_mcp_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"])
    print("MCP server parameters initialized")
    
    try:
        print("\nAttempting to create MCP workbench...")
        # Create an MCP workbench which provides a session to the mcp server
        async with McpWorkbench(fetch_mcp_server) as workbench:
            print("MCP workbench created successfully")
            
            print("\nInitializing OpenAI client...")
            # Create an agent that can use the fetch tool
            model_client = OpenAIChatCompletionClient(
                model="gpt-4.1-nano",
                api_key=os.getenv("OPENAI_API_KEY")
            )
            print("OpenAI client initialized")
            
            print("\nCreating fetch agent...")
            fetch_agent = AssistantAgent(
                name="fetcher",
                model_client=model_client,
                workbench=workbench,
                reflect_on_tool_use=True
            )
            print("Fetch agent created")

            print("\nStarting URL fetch and summarize task...")
            # Let the agent fetch the content of a URL and summarize it
            result = await fetch_agent.run(task="Summarize the content of https://en.wikipedia.org/wiki/Seattle")
            print("Task completed")
            
            if isinstance(result.messages[-1], TextMessage):
                print("\n=== Summary ===")
                print(result.messages[-1].content)
                print("=== End Summary ===")
            else:
                print("Unexpected message type received")
                print(f"Message type: {type(result.messages[-1])}")

            print("\nClosing model client...")
            # Close the connection to the model client
            await model_client.close()
            print("Model client closed")
            
    except Exception as e:
        print(f"\nERROR: An error occurred: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
    finally:
        # Ensure any cleanup is performed
        print("\n=== Cleanup completed ===")

if __name__ == "__main__":
    print("\n=== Script execution started ===")
    try:
        # Run the async main function
        asyncio.run(main())
    except Exception as e:
        print(f"\nCRITICAL ERROR: Failed to run main function: {str(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
    print("\n=== Script execution completed ===")