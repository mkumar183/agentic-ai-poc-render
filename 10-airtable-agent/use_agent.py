import json
from agent_auth import AirtableAgent

def get_base_id_by_name(bases_data: dict, base_name: str) -> str:
    """Get the base ID for a given base name."""
    for base in bases_data.get('bases', []):
        if base.get('name') == base_name:
            return base.get('id')
    raise ValueError(f"Base with name '{base_name}' not found")

def main():
    # Load tokens from file
    try:
        with open('airtable_tokens.json', 'r') as f:
            token_info = json.load(f)
    except FileNotFoundError:
        print("Error: airtable_tokens.json not found. Please run get_tokens.py first.")
        return

    # Create and initialize agent
    agent = AirtableAgent("my-agent")
    agent.set_initial_tokens(
        access_token=token_info['access_token'],
        refresh_token=token_info['refresh_token'],
        expires_in=token_info['expires_in']
    )

    try:
        # List all bases
        print("Listing bases...")
        bases = agent.list_bases()
        print("Available bases:", bases)

        # Get base ID for "Nuragi"
        base_id = get_base_id_by_name(bases, "Nuragi")
        print(f"\nFound base ID for Nuragi: {base_id}")
        
        # List leads in the base
        print(f"\nListing leads in base {base_id}...")
        leads = agent.list_leads(base_id)
        print("Leads:", leads)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 