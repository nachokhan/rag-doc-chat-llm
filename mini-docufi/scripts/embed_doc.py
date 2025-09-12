import os
import sys
import tempfile

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session

from app import models
from app.db import SessionLocal
from app.services import embeddings, facts
from app.utils import parser_docx, parser_pdf

def embed_document(file_path: str, db: Session):
    """Processes and embeds a single document."""
    try:
        filename = os.path.basename(file_path)
        # Parse the document based on file type
        if filename.endswith(".pdf"):
            pages_content = parser_pdf.parse_pdf(file_path)
        elif filename.endswith(".docx"):
            pages_content = parser_docx.parse_docx(file_path)
        else:
            print("Unsupported file type")
            return

        # Create a new document record
        doc = models.Document(filename=filename)
        db.add(doc)
        db.commit()
        db.refresh(doc)

        page_embeddings = embeddings.generate_embeddings(pages_content)

        for i, content in enumerate(pages_content):
            page_number = i + 1
            # Create a new page record
            page = models.Page(
                document_id=doc.id,
                page_number=page_number,
                content=content,
                embedding=page_embeddings[i]
            )
            db.add(page)

            # Extract facts from the page
            extracted_facts = facts.get_facts_from_text(content)
            if extracted_facts:
                fact_texts = [f'{f.get("label", "")}: {f.get("value_text", "")}' for f in extracted_facts]
                fact_embeddings = embeddings.generate_embeddings(fact_texts)

                for j, fact_data in enumerate(extracted_facts):
                    fact = models.Fact(
                        document_id=doc.id,
                        label=fact_data.get("label", ""),
                        value_text=fact_data.get("value_text", ""),
                        page=page_number,
                        embedding=fact_embeddings[j]
                    )
                    db.add(fact)

        db.commit()
        print(f"Successfully embedded document: {filename} (docId: {doc.id})")

    except Exception as e:
        db.rollback()
        print(f"Error embedding document: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/embed_doc.py <path_to_document>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    db = SessionLocal()
    try:
        embed_document(file_path, db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
