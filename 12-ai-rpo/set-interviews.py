# In this program we will schedule interviews for candidates and send them an email with the interview details
# for setting up interview use mailgun api https://ai-recruiter.micro1.ai/api-reference/getting-started/introduction
# we will use the mailgun api to schedule the interview and send the email
# we will use the airtable api to get the candidates from the airtable base
# we will use the openai api to get the interview details

from airtable import Airtable # https://pypi.org/project/airtable/
from dotenv import load_dotenv
import os
import requests

def init_airtable():
    """Initialize Airtable client with environment variables."""
    load_dotenv()

    API_KEY = os.getenv('AIRTABLE_API_KEY')
    BASE_ID = os.getenv('AIRTABLE_BASE_ID')
    
    airtable = Airtable(BASE_ID, API_KEY)
    return airtable
        
def list_tables():
    """List all tables in the Airtable base."""
    load_dotenv()
    
    API_KEY = os.getenv('AIRTABLE_API_KEY')
    BASE_ID = os.getenv('AIRTABLE_BASE_ID')
    
    # Airtable API endpoint for base metadata
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tables = response.json()
        
        print("\nAvailable tables in your base:")
        print("-" * 40)
        for table in tables.get('tables', []):
            print(f"Table Name: {table.get('name')}")
            print(f"Table ID: {table.get('id')}")
            print("-" * 40)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tables: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")

def schedule_interview(interview_name, skills, custom_questions_list, coding_language="python", 
                       interview_language="en", 
                       can_change_interview_language=False, 
                       only_coding_round=False, 
                       is_coding_round_required=False, 
                       selected_coding_language="python", 
                       coding_exercise_details="Make the DSA problem extremely difficult and focus on a problem that will require recursion to solve efficiently.", 
                       is_proctoring_required=True):
    """
    Schedule an interview using the Micro1 API.
    
    Args:
        candidate_name (str): Name of the candidate
        skills (list): List of dictionaries containing skill name and description
        custom_questions (list): List of dictionaries containing question details
        interview_language (str): Language for the interview
        coding_required (bool): Whether coding round is required
        coding_language (str): Programming language for coding round
        proctoring_required (bool): Whether proctoring is required
    
    Returns:
        dict: Response from the API
    """
    url = "https://public.api.micro1.ai/interview"
    
    payload = {
        "interview_name": interview_name,
        "skills": skills,
        "custom_question_list": custom_questions,
        "interview_language": interview_language,
        "can_change_interview_language": False,
        "only_coding_round": coding_required,
        "is_coding_round_required": coding_required,
        "selected_coding_language": coding_language,
        "coding_exercise_details": "Make the DSA problem extremely difficult and focus on a problem that will require recursion to solve efficiently.",
        "is_proctoring_required": proctoring_required
    }
    
    headers = {
        "x-api-key": os.getenv('MICRO1_API_KEY'),
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error scheduling interview: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None


def process_candidates():
    try:
        airtable = init_airtable()
        
        records = airtable.get('Applicants')  

        if not records:
            print("No records found in the table")
            return

        for record in records.get('records', []):
            fields = record.get('fields', {})
            candidate_name = fields.get('Name')
            status = fields.get('Status')
            
            if status == 'Ready for Interview':
                print(f"Scheduling interview for {candidate_name}")
                # ... call your interview scheduling function/module
            else:
                print(f"Candidate {candidate_name} status: {status}")

    except Exception as e:
        print(f"Error processing candidates: {str(e)}")
        raise

# for candidates schedule their interviews and send them an email with the interview details
# for setting up interview use mailgun api https://ai-recruiter.micro1.ai/api-reference/getting-started/introduction








if __name__ == "__main__":
    # list_tables()
    # process_candidates()  # Uncomment after you've identified the correct table name
    # schedule_interview()
    interview_name = "Full Stack Engineer Interview"
    skills = [
        {
            "name": "React",
            "description": "Must be proficient in React Context API"
        }
    ]
    custom_question_list = [
        {
            "question": "What are your strengths and weaknesses?",
            "time": 2,
            "type": "audio"
        }
    ]
    interview_language = "en"
    can_change_interview_language = False
    only_coding_round = False
    is_coding_round_required = False
    selected_coding_language = "python"
    coding_exercise_details = "Make the DSA problem extremely difficult and focus on a problem that will require recursion to solve efficiently."
    is_proctoring_required= True


# user_choice, javascript, cpp, c, csharp, go, java, kotlin, php, python, ruby, rust, swift, typescript
def schedule_interview(interview_name, skills, custom_questions_list, coding_language="python",                                                                      
                       is_coding_round_required=False, 
                       selected_coding_language="user_choice", 
                       coding_exercise_details="Make the DSA problem extremely difficult and focus on a problem that will require recursion to solve efficiently.", 
                       is_proctoring_required=True):




    interview_details = schedule_interview(interview_name=interview_name, 
                        skills=skills, 
                        custom_question_list=custom_question_list, 
                        coding_language="python", 
                        coding_exercise_details=coding_exercise_details, 
                        is_proctoring_required=is_proctoring_required
                        )

    print(interview_details)