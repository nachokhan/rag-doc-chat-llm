"""
Researcher agent for the market analysis service.
"""
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent

from app.services.tools import all_tools # Updated import
from . import prompts

# Initialize the LLM
llm = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview", api_key=os.getenv("OPENAI_API_KEY"))

# Create the researcher agent
researcher_agent_runnable = create_openai_tools_agent(
    llm=llm,
    tools=all_tools, # Use the aggregated list
    prompt=prompts.RESEARCHER_PROMPT
)

# Create the Agent Executor
researcher_agent = AgentExecutor(
    agent=researcher_agent_runnable,
    tools=all_tools, # Use the aggregated list
    verbose=True # Set to True for debugging to see the agent's thought process
)

def run_research(topic: str):
    """
    Runs the researcher agent on a given topic.
    """
    print(f"Running researcher agent for topic: {topic}")
    response = researcher_agent.invoke({"input": topic})
    return response["output"]
