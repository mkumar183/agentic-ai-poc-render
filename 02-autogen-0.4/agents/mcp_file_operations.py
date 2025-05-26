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
    
    # Get the basic MCP server
    print("Initializing MCP server parameters...")
    mcp_server = StdioServerParams(command="uvx", args=["mcp-server"])
    print("MCP server parameters initialized")
    
    try:
        print("\nAttempting to create MCP workbench...")
        async with McpWorkbench(mcp_server) as workbench:
            print("MCP workbench created successfully")
            
            print("\nInitializing OpenAI client...")
            model_client = OpenAIChatCompletionClient(
                model="gpt-4.1-nano",
                api_key=os.getenv("OPENAI_API_KEY")
            )
            print("OpenAI client initialized")
            
            print("\nCreating file operations agent...")
            file_agent = AssistantAgent(
                name="file_operator",
                model_client=model_client,
                workbench=workbench,
                reflect_on_tool_use=True
            )
            print("File operations agent created")

            # Create a test file
            test_file = "test_data.txt"
            print(f"\nCreating test file: {test_file}")
            with open(test_file, "w") as f:
                f.write("This is a test file.\nIt contains multiple lines.\nWe will use MCP to read and process this file.")
            print("Test file created successfully")

            print("\nStarting file operations task...")
            print("Sending task to agent...")
            result = await file_agent.run(
                task=f"List the contents of the current directory and then read the file '{test_file}'"
            )
            print("Task completed")
            
            if isinstance(result.messages[-1], TextMessage):
                print("\n=== Result ===")
                print(result.messages[-1].content)
                print("=== End Result ===")
            else:
                print("Unexpected message type received")
                print(f"Message type: {type(result.messages[-1])}")

            # Clean up the test file
            if os.path.exists(test_file):
                os.remove(test_file)
                print(f"\nCleaned up test file: {test_file}")

            print("\nClosing model client...")
            await model_client.close()
            print("Model client closed")
            
    except Exception as e:
        print(f"\nERROR: An error occurred: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
    finally:
        print("\n=== Cleanup completed ===")

if __name__ == "__main__":
    print("\n=== Script execution started ===")
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\nCRITICAL ERROR: Failed to run main function: {str(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
    print("\n=== Script execution completed ===") 