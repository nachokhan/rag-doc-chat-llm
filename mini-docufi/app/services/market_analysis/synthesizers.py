"""
Synthesizer chains for the market analysis service.
"""
import os
import logging
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from . import prompts

# Initialize the LLM
llm = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview", api_key=os.getenv("OPENAI_API_KEY"))

# Create the chains using LangChain Expression Language (LCEL)
market_size_chain = prompts.MARKET_SIZE_SYNTHESIZER_PROMPT | llm | StrOutputParser()
top_players_chain = prompts.TOP_PLAYERS_SYNTHESIZER_PROMPT | llm | StrOutputParser()

def synthesize_market_size(data: str) -> str:
    """
    Runs the market size synthesis chain on the given data.
    """
    logging.info("Synthesizing market size...")
    return market_size_chain.invoke({"context": data})

def synthesize_top_players(data: str) -> str:
    """
    Runs the top players synthesis chain on the given data.
    """
    logging.info("Synthesizing top players...")
    return top_players_chain.invoke({"context": data})