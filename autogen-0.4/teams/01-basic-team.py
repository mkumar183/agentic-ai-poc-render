import asyncio
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Task:
    """Represents a task to be executed by the team."""
    name: str
    description: str
    is_stream: bool = False
    external_termination: bool = False

def print_messages(messages: List[TextMessage]):
    """Print messages in a nicely formatted way."""
    print("\n" + "="*80)
    print("CONVERSATION LOG")
    print("="*80)
    
    for msg in messages:
        print(f"\n[{msg.source.upper()}]")
        print("-" * 40)
        print(msg.content)
        if msg.models_usage:
            print(f"\nTokens used: {msg.models_usage.prompt_tokens} prompt, {msg.models_usage.completion_tokens} completion")
        print("-" * 40)
    
    print("\n" + "="*80)

def create_model_client() -> OpenAIChatCompletionClient:
    """Create and return an OpenAI model client."""
    return OpenAIChatCompletionClient(
        model="gpt-4o-2024-08-06",
        api_key=os.getenv("OPENAI_API_KEY")
    )

def create_agents(model_client: OpenAIChatCompletionClient) -> Tuple[AssistantAgent, AssistantAgent]:
    """Create and return the primary and critic agents."""
    primary_agent = AssistantAgent(
        "primary",
        model_client=model_client,
        system_message="You are a helpful AI assistant.",
    )

    critic_agent = AssistantAgent(
        "critic",
        model_client=model_client,
        system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed.",
    )
    
    return primary_agent, critic_agent

def create_team(primary_agent: AssistantAgent, critic_agent: AssistantAgent) -> RoundRobinGroupChat:
    """Create and return a team with the given agents."""
    text_termination = TextMentionTermination("APPROVE")
    external_termination = ExternalTermination()
    return RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=external_termination | text_termination)

async def run_task(team: RoundRobinGroupChat, task: Task) -> Any:
    """Run a single task with the team."""
    print(f"\n=== Running {task.name} ===")
    await team.reset()  # Reset the team for a new task
    
    if task.is_stream:
        if task.external_termination:
            # Create external termination condition for this task
            external_termination = ExternalTermination()            
            
            # Run the team in a background task
            run = asyncio.create_task(Console(team.run_stream(task=task.description)))
            
            # Wait for some time
            await asyncio.sleep(5)  # Wait for 5 seconds
            
            # Stop the team
            print("\n=== External Termination Triggered ===")
            external_termination.set()
            
            # Wait for the team to finish
            await run
            return None
        else:
            async for message in team.run_stream(task=task.description):  # type: ignore
                if isinstance(message, TaskResult):
                    print("Stop Reason:", message.stop_reason)
                else:            
                    print_messages([message])
            return None
    else:
        result = await team.run(task=task.description)
        print_messages(result.messages)
        print(f"\nStop reason: {result.stop_reason}")
        return result

async def run_tasks(team: RoundRobinGroupChat, tasks: List[Task]) -> List[Any]:
    """Run multiple tasks with the team."""
    results = []
    for task in tasks:
        result = await run_task(team, task)
        results.append(result)
    return results

async def main():
    # Define tasks
    tasks = [
        # Task(
        #     name="Streaming Poem Task",
        #     description="Write a short poem about the fall season.",
        #     is_stream=True
        # ),
        Task(
            name="Externally Terminated Task",
            description="Write a detailed analysis of climate change impacts. This will be a long response that we'll terminate externally.",
            is_stream=True,
            external_termination=True
        )
    ]
    
    # Create model client
    model_client = create_model_client()
    
    try:
        # Create agents
        primary_agent, critic_agent = create_agents(model_client)
        
        # Create team
        team = create_team(primary_agent, critic_agent)
        
        # Run all tasks
        results = await run_tasks(team, tasks)
        
    finally:
        # Clean up
        await model_client.close()

if __name__ == "__main__":
    asyncio.run(main())

