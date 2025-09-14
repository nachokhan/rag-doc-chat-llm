"""
Tools for the market analysis agents.
"""
import os
import logging
from langchain.tools import tool
from app.services import embeddings
from app import models
from app.db import get_db

# This is a placeholder for the actual google_web_search tool.
# In a real scenario, this would be the tool provided by the environment.
class MockGoogleWebSearch:
    def search(self, query: str):
        return f"Mock search results for: {query}"

google_web_search = MockGoogleWebSearch()

CREDIBLE_SOURCES = [
    "gartner.com",
    "idc.com",
    "forrester.com",
    "bloomberg.com",
    "reuters.com",
    "worldbank.org",
    "statista.com",
    "forbes.com",
]

@tool
def external_search(query: str) -> str:
    """Searches credible external sources for information on a given topic."""
    logging.info(f"Executing external search for: {query}")
    site_queries = " OR ".join([f"site:{source}" for source in CREDIBLE_SOURCES])
    full_query = f'"{query}" ({site_queries})'

    # In a real scenario, this would call the actual google_web_search tool.
    # For this implementation, we call the mock version.
    search_results = google_web_search.search(query=full_query)

    # Here you could also process the results, e.g., by fetching and summarizing the content of the top URLs.
    # For now, we'll just return the raw search results.
    return search_results

@tool
def internal_search(query: str) -> str:
    """Searches internal documents (pages and facts) for information on a given topic."""
    logging.info(f"Executing internal search for: {query}")
    db = next(get_db())
    try:
        query_embedding = embeddings.generate_embeddings([query])[0]

        # Search across all pages in the database
        pages_with_distance = (
            db.query(
                models.Page,
                models.Page.embedding.l2_distance(query_embedding).label("distance")
            )
            .order_by("distance")
            .limit(5)
            .all()
        )

        # Search across all facts in the database
        facts_with_distance = (
            db.query(
                models.Fact,
                models.Fact.embedding.l2_distance(query_embedding).label("distance")
            )
            .order_by("distance")
            .limit(10)
            .all()
        )

        page_context = "\n".join([f"[Page {p.page_number} from doc {p.document_id}]: {p.content}" for p, dist in pages_with_distance])
        fact_context = "\n".join([f"[Fact from doc {f.document_id}]: {f.label}: {f.value_text}" for f, dist in facts_with_distance])

        if not page_context and not fact_context:
            return "No relevant information found in internal documents."

        return f"""Relevant Information from Internal Documents:

---
From Document Pages ---
{page_context}

---
From Extracted Facts ---
{fact_context}
"""
    finally:
        db.close()
