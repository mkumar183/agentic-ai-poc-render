import os
from dotenv import load_dotenv
import autogen
import logging

# Enable debugging logs
# Enable debugging logs and write to a file
log_filename = 'book_writing_workflow.log'
logging.basicConfig(level=logging.DEBUG, filename=log_filename, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')


# Load environment variables
load_dotenv()

# Get the OpenAI API key from the environment
api_key = os.environ.get("OPENAI_API_KEY")

# Define the LLM configuration
llm_config = {
    "model": "gpt-3.5-turbo",
    "api_key": api_key,
}

# Define the main controller agent
controller = autogen.UserProxyAgent(
    name="controller", 
    is_termination_msg=lambda x: x.get("content", "") == "DONE",
    llm_config=llm_config,
    code_execution_config={
        "workd_dir": "code_execution",
        "use_docker": False,
    },    
    )

# Content Writing Agent
content_writer = autogen.AssistantAgent(
    name="content_writer",
    system_message= """You are a technical leadership book-writing AI expert writing one chapter at a time. 
                       Expand rough content into structured, 
                       detailed chapter with narratives and examples. 
                       Ensure the chapter is around 5000 words."""
    ,
    llm_config=llm_config,
)

# Case Study Generator
case_study_agent = autogen.AssistantAgent(
    name="case_study_agent", 
    system_message="You provide real-world leadership case studies relevant to each book topic.",
    llm_config=llm_config,
    )

# Narrative Agent
narrative_agent = autogen.AssistantAgent(
    name="narrative_agent",
    system_message="You add engaging narratives or stories from the real world to illustrate the key points in the chapter.",
    llm_config=llm_config,
)

# Editing & Refinement Agent
editor = autogen.AssistantAgent(
    name="editor", 
    system_message="You refine writing, ensuring clarity, coherence, and a professional tone.",
    llm_config=llm_config,
    )

# Summary Agent
summarizer = autogen.AssistantAgent(
    name="summarizer", 
    system_message="You generate concise summaries and key takeaways for each chapter.",
    llm_config=llm_config,
    )

# Formatting Agent
formatter = autogen.AssistantAgent(
    name="formatter", 
    system_message="You format the chapter content into a structured, professional layout.",
    llm_config=llm_config,
    )


# Workflow Logic: Connect the Agents
def book_writing_workflow(dimension_content):
    """Automates the book-writing process."""
    print("Step 1: Expanding content...")
    logging.debug("Sending message to content_writer: %s", dimension_content)
    expanded_chapter = controller.initiate_chat(content_writer, message=dimension_content)
    logging.debug("Received response from content_writer: %s", expanded_chapter)
    print("Expanded Chapter Content:\n", expanded_chapter)

    print("Step 2: Adding narratives...")
    logging.debug("Sending message to narrative_agent: %s", expanded_chapter)
    narratives = controller.initiate_chat(narrative_agent, message=expanded_chapter)
    logging.debug("Received response from narrative_agent: %s", narratives)
    print("Narratives:\n", narratives)

    print("Step 3: Adding case studies...")
    logging.debug("Sending message to case_study_agent: %s", expanded_chapter + "\n" + narratives)
    case_study = controller.initiate_chat(case_study_agent, message=expanded_chapter + "\n" + narratives)
    logging.debug("Received response from case_study_agent: %s", case_study)
    print("Case Study:\n", case_study)

    print("Step 4: Editing & Refinement...")
    logging.debug("Sending message to editor: %s", expanded_chapter + "\n" + narratives + "\n" + case_study)
    refined_content = controller.initiate_chat(editor, message=expanded_chapter + "\n" + narratives + "\n" + case_study)
    logging.debug("Received response from editor: %s", refined_content)
    print("Refined Content:\n", refined_content)

    print("Step 5: Summarization...")
    logging.debug("Sending message to summarizer: %s", refined_content)
    summary = controller.initiate_chat(summarizer, message=refined_content)
    logging.debug("Received response from summarizer: %s", summary)
    print("Summary:\n", summary)

    print("Step 6: Formatting...")
    logging.debug("Sending message to formatter: %s", refined_content + "\n\nSummary:\n" + summary)
    final_version = controller.initiate_chat(formatter, message=refined_content + "\n\nSummary:\n" + summary)
    logging.debug("Received response from formatter: %s", final_version)
    print("Final Version:\n", final_version)
    final_version = expanded_chapter

    return final_version


# Example usage with your dimension content
dimension_content = """
Write a structured and detailed chapter (5000 words) on 'Building a Culture of Teamwork and Autonomy' in high-performing teams. 
This chapter precedes the chapter about setting team structures right and aligning each team around goals such that each team can operate with as much autonomy as possible. 
Use a clear, engaging, and insightful tone that aligns with leadership and organizational growth. The content should include the following key areas:

1️⃣ Importance of Collaboration:

Explain how the most important aspect of a team is the collaboration between team members.
Discuss how effective communication, such as code reviews, design reviews, and brainstorming on architecture, improves the outcome of the work performed by each person.
Highlight how cross-functional and cross-skilled interactions enhance the team's overall performance towards the team goal.

2️⃣ Building Psychological Safety:

Detail the importance of creating a psychologically safe environment where team members feel safe to express ideas and concerns.
Provide strategies for building psychological safety within the team.

3️⃣ Pro-Social Cause and Shared Understanding:

Discuss the role of a pro-social cause in keeping the team motivated.
Explain the importance of a shared understanding of goals and business context.

4️⃣ Frameworks and Models:

Reference excellent frameworks such as Patrick Lencioni’s Five Dysfunctions of a Team.
Analyze how these frameworks can be applied to eliminate common team dysfunctions:
Absence of trust
Fear of conflict
Lack of commitment
Avoidance of accountability
Inattention to results

5️⃣ Enhancing Team Chemistry:

Emphasize the importance of team-building activities and their purpose in building trust and respect between members.
Discuss the significance of paying attention to the tone of communication to ensure respectful and constructive interactions.

6️⃣ Case Study or Example:

Provide a real-world or hypothetical example of a team that improved through empowerment, trust, and strong collaboration.

Writing Style & Format:

Engaging and leadership-focused (like a management book).
Actionable insights with real-world relevance.
Use subheadings, bullet points, and key takeaways for clarity.
"""
final_chapter = book_writing_workflow(dimension_content)
print("\nFinal Chapter Content:\n", final_chapter)