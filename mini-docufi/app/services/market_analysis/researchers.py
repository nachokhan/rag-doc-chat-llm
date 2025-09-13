"""
Researcher agents for the market analysis service.
"""

from . import tools

def research_external_data(query: str):
    """
    Researches external data using the web.
    """
    print(f"Researching external data for: {query}")
    return tools.external_search(query)

def research_internal_data(query: str):
    """
    Researches internal data from the user's documents.
    """
    print(f"Researching internal data for: {query}")
    return tools.internal_search(query)
