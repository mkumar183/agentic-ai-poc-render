import os, json
from autogen import ConversableAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
from psychological_safety import blog

load_dotenv()

llm_config = {
    "model": "gpt-4o",
    "temperature": 0.9,
    "api_key": os.environ["OPENAI_API_KEY"],
}

# Serialize the blog object to JSON
blog_json = json.dumps(blog.to_dict(), indent=4)
print(blog_json)

blog_intro_agent = ConversableAgent(
    name="Blog_Intro_Agent",
    system_message=blog_json,
    llm_config=llm_config,
    description="Provides the initial content of the blog.",
)

review_agent = ConversableAgent(
    name="Review_Agent",
    system_message="""
        You are a Blog Review Agent. Your role is to evaluate each blog and provide actionable feedback to improve the overall quality of the content. Please review the blog based on the following criteria and instruct the finalizer agent accordingly:
        Title & Introduction:
        Ensure the title is compelling and the introduction is engaging.
        
        Problem Statement & Analysis:
        Confirm there is a clear problem statement and a deep dive into the problem.
        Check that the explanation includes why the solution is needed.
        Proposed Solution & Implementation:

        Evaluate the proposed solution, implementation details, technical .

        Supporting Content: real life case studies, references and measurable indicators:
        Ensure there are good case studies, references and measurable indicators.
        Ensure there are methods for measuring the success of the solution.                
        Check for measurable indicators for both the problem and the solution; if absent, prompt the finalizer to include them.
        Ensure there are references backing up the claims. If not, instruct the finalizer to incorporate credible sources.
        
        Headings and Subheadings:
        Ensure unnecessary headings and subheadings are removed and that the remaining ones are clear and relevant. 
        the ones that is provided in initial structure are for guidance only. such as blog should not have heading hook. 

        Conclusion:
        Confirm the conclusion is compelling and includes a clear call to action. If not, request improvements from the finalizer.
        
        Overall Length:
        Ensure the blog is approximately 5,000 words. If it falls short, ask the finalizer to expand the content.
        Provide concise, actionable feedback based on these criteria to guide improvements.
        """,
    llm_config=llm_config,
description="Reviews the blog and calls other agents to improve the blog.",)

finalize_blog = ConversableAgent(
    name="Finalize_Blog",
    system_message="""Based on the detailed instructions provided by the Review Agent, your task is to refine, polish, and finalize the blog post. Incorporate all feedback to ensure:
    
    - A compelling and attention-grabbing title
    - An engaging introduction that draws readers in
    - A clear, concise, and deep problem statement
    - A thorough analysis of the problem and a well-justified need for a solution
    - A detailed proposed solution, including implementation details, technical breakdown, and relevant use cases
    - Inclusion of real-life case studies, measurable indicators, and credible references
    - A compelling conclusion that includes a strong call to action
    
    Ensure the final blog is cohesive, professionally written, and meets the target length of approximately 5,000 words. Continue iterating and improving the content until it is publication-ready.
    """,
    llm_config=llm_config,
    description="Finalize and polish the blog post by integrating all feedback from the review agent, producing a cohesive and publication-ready blog.",
)

# Create a Group Chat
group_chat = GroupChat(
    agents=[
        blog_intro_agent,
        review_agent, 
        finalize_blog
    ],
    messages=[],
    max_round=10,
)

# Create a Group Chat Manager
group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
)

# Initiate the chat with an initial message
chat_result = blog_intro_agent.initiate_chat(
    group_chat_manager,
    message="""I want to write a blog post on 
    - Importance of psychological safety in technical scrum teams for LinkedIn. 
    - Target Audience is Engineering Leaders
    - Context is Technical Scrum Team doing complex problem solving and creative work. Coding, Designing. 
    - Goal is to show case importance of psychological safety in teams for improving innovation and collaboration.
    - Length should be about 5000 words.     
    """,
    summary_method="reflection_with_llm",
)

# print final blog
print(chat_result.summary)