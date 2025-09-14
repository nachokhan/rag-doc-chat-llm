"""
Tool discovery and aggregation.
"""
from .external_search import external_search
from .internal_search import internal_search

all_tools = [external_search, internal_search]
