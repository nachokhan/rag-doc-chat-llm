"""
Internal search tool.
"""
from langchain.tools import tool
from app.services import embeddings
from app import models
from app.db import get_db

@tool
def internal_search(query: str) -> str:
    """Searches internal documents (pages and facts) for information on a given topic."""
    print(f"Executing internal search for: {query}")
    db = next(get_db())
    try:
        query_embedding = embeddings.generate_embeddings([query])[0]
        pages_with_distance = db.query(models.Page, models.Page.embedding.l2_distance(query_embedding).label("distance")).order_by("distance").limit(5).all()
        facts_with_distance = db.query(models.Fact, models.Fact.embedding.l2_distance(query_embedding).label("distance")).order_by("distance").limit(10).all()
        page_context = "\n".join([f"[Page {p.page_number} from doc {p.document_id}]: {p.content}" for p, dist in pages_with_distance])
        fact_context = "\n".join([f"[Fact from doc {f.document_id}]: {f.label}: {f.value_text}" for f, dist in facts_with_distance])
        if not page_context and not fact_context:
            return "No relevant information found in internal documents."
        return f"""Relevant Information from Internal Documents:

--- From Document Pages ---
{page_context}

--- From Extracted Facts ---
{fact_context}
"""
    finally:
        db.close()

