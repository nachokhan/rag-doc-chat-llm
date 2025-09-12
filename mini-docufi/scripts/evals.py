import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services import chat


def main():
    """Runs a simple evaluation of the chat service."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/evals.py <docId>")
        sys.exit(1)

    doc_id = sys.argv[1]

    questions = [
        "What is the main topic of the document?",
        "What are the key findings?",
        "What is the conclusion?",
    ]

    db = SessionLocal()
    try:
        for question in questions:
            print(f"\nQuestion: {question}")
            response = chat.get_chat_response(db, doc_id, question)
            print(f"Answer: {response['reply']}")
            print(f"Sources: {response['Sources']}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
