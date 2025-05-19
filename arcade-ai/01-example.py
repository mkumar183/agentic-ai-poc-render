from arcadepy import Arcade
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def initialize_arcade():
    """Initialize the Arcade client with API key."""
    arcade_api_key = os.getenv("ARCADE_API_KEY")
    if not arcade_api_key:
        raise ValueError("ARCADE_API_KEY environment variable is not set")
    return Arcade(api_key=arcade_api_key)

def execute_math_tool(client: Arcade, user_id: str):
    """Demonstrate using the Math.Sqrt tool."""
    print("\n=== Math Tool Example ===")
    try:
        response = client.tools.execute(
            tool_name="Math.Sqrt",
            input={"a": '625'},
            user_id=user_id,
        )
        print(f"The square root of 625 is {response.output.value}")
    except Exception as e:
        print(f"Error executing math tool: {e}")

def handle_github_auth(client: Arcade, user_id: str):
    """Handle GitHub authentication and repository operations."""
    print("\n=== GitHub Authentication Example ===")
    try:
        # Request GitHub authorization
        auth_response = client.tools.authorize(
            tool_name="GitHub.ListOrgRepositories",
            user_id=user_id,
        )
        
        if auth_response.status != "completed":
            print(f"Please click this link to authorize: {auth_response.url}")
            print("Waiting for authorization...")
            client.auth.wait_for_completion(auth_response.id)
            print("Authorization completed!")
        
        return True
    except Exception as e:
        print(f"Error during GitHub authentication: {e}")
        return False

def list_github_repos(client: Arcade, user_id: str, username: str):
    """List GitHub repositories for a user."""
    try:
        response = client.tools.execute(
            tool_name="GitHub.ListRepositories",
            input={
                "username": username,
                "type": "all",  # Can be 'all', 'owner', 'member'
                "sort": "updated",  # Can be 'created', 'updated', 'pushed', 'full_name'
                "direction": "desc",  # Can be 'asc' or 'desc'
                "per_page": 10  # Number of repos to list
            },
            user_id=user_id,
        )
        
        if response.success:
            print(f"\n=== Repositories for {username} ===")
            repos = response.output.value
            for repo in repos:
                print(f"\nRepository: {repo['name']}")
                print(f"Description: {repo.get('description', 'No description')}")
                print(f"Stars: {repo.get('stargazers_count', 0)}")
                print(f"URL: {repo.get('html_url', 'N/A')}")
            print(f"\nResponse: {response}")
        else:
            print(f"Failed to list repositories. Error: {response.output.error.message if response.output.error else 'Unknown error'}")
            
    except Exception as e:
        print(f"Error listing repositories: {e}")

def main():
    # Initialize Arcade client
    client = initialize_arcade()
    
    # Use your email as the user ID
    user_id = "mkumar183@gmail.com"
    
    # Execute math tool example
    execute_math_tool(client, user_id)
    
    # Handle GitHub authentication
    if handle_github_auth(client, user_id):
        # List repositories
        list_github_repos(client, user_id, "mkumar183")
    
    print("\n=== Example Completed ===")

if __name__ == "__main__":
    main()