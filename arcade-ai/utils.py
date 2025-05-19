from arcadepy import Arcade
import os
from dotenv import load_dotenv
from typing import Optional

def init_arcade_client(api_key: Optional[str] = None) -> Arcade:
    """
    Initialize and return an Arcade client.
    
    Args:
        api_key (str, optional): Explicit API key. If not provided, will try to load from environment.
        
    Returns:
        Arcade: Initialized Arcade client
        
    Raises:
        ValueError: If no API key is found in environment or provided
    """
    # Load environment variables
    load_dotenv()
    
    # Use provided API key or try to get from environment
    arcade_api_key = api_key or os.getenv("ARCADE_API_KEY")
    
    if not arcade_api_key:
        raise ValueError("No API key provided. Set ARCADE_API_KEY environment variable or provide api_key parameter.")
    
    return Arcade(api_key=arcade_api_key) 