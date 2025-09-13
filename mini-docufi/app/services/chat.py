import os
from openai import OpenAI
from sqlalchemy.orm import Session

from app import models
from app.services import embeddings

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_chat_response(db: Session, doc_id: str, message: str) -> dict:
    """Generates a chat response based on a user's message and a document."""
    message_embedding = embeddings.generate_embeddings([message])[0]

    # Find relevant pages
    pages_with_distance = (
        db.query(
            models.Page,
            models.Page.embedding.l2_distance(message_embedding).label("distance")
        )
        .filter(models.Page.document_id == doc_id)
        .order_by("distance")
        .limit(3)
        .all()
    )
    relevant_pages = [page for page, distance in pages_with_distance]


    # Find relevant facts
    facts_with_distance = (
        db.query(
            models.Fact,
            models.Fact.embedding.l2_distance(message_embedding).label("distance")
        )
        .filter(models.Fact.document_id == doc_id)
        .order_by("distance")
        .limit(5)
        .all()
    )
    relevant_facts = [fact for fact, distance in facts_with_distance]

    # Construct the prompt
    context = "\n".join([p.content for p in relevant_pages])
    facts = "\n".join([f'{f.label}: {f.value_text}' for f in relevant_facts])
    prompt = f"""Answer the following question based on the provided context and facts.

Context:
{context}

Facts:
{facts}

Question: {message}

Answer:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about documents."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    reply = response.choices[0].message.content

    sources = {
        "facts": [
            {"id": str(f.id), "label": f.label, "value_text": f.value_text, "page": f.page, "score": d}
            for f, d in facts_with_distance
        ],
        "pages": [
            {"page": p.page_number, "score": d} for p, d in pages_with_distance
        ]
    }

    return {"reply": reply, "Sources": sources}
