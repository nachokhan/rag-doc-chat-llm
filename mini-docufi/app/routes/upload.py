import logging
import os
import tempfile
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.services import embeddings, facts
from app.utils import parser_docx, parser_pdf

router = APIRouter()

@router.post("/upload")
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Uploads a document, parses it, extracts facts, generates embeddings, and saves everything to the database."""
    try:
        logging.info("Received file: %s", file.filename)

        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        # Parse the document based on file type
        if file.filename.endswith(".pdf"):
            pages_content = parser_pdf.parse_pdf(tmp_path)
        elif file.filename.endswith(".docx"):
            pages_content = parser_docx.parse_docx(tmp_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Create a new document record
        logging.info("Creating document record in the database...")
        doc = models.Document(filename=file.filename)
        db.add(doc)
        db.commit()
        db.refresh(doc)

        page_embeddings = embeddings.generate_embeddings(pages_content)

        logging.info("Storing pages and extracting facts...")
        for i, content in enumerate(pages_content):
            page_number = i + 1
            # Create a new page record
            logging.info("Creating page %d record in the database...", page_number)
            page = models.Page(
                document_id=doc.id,
                page_number=page_number,
                content=content,
                embedding=page_embeddings[i]
            )
            logging.info("Storing page %d in the database...", page_number)
            db.add(page)

            # Extract facts from the page
            logging.info("Extracting facts from page... %d", page_number)
            extracted_facts = facts.get_facts_from_text(content)

            if extracted_facts:
                fact_texts = [f'{f.get("label", "")}: {f.get("value_text", "")}' for f in extracted_facts]
                fact_embeddings = embeddings.generate_embeddings(fact_texts)

                for j, fact_data in enumerate(extracted_facts):
                    logging.info("Storing fact in the database: %s", fact_data)
                    fact = models.Fact(
                        document_id=doc.id,
                        label=fact_data.get("label", ""),
                        value_text=fact_data.get("value_text", ""),
                        page=page_number,
                        embedding=fact_embeddings[j]
                    )
                    db.add(fact)

        db.commit()
        logging.info("Upload and processing completed successfully for document ID: %s", doc.id)

        return {"docId": str(doc.id)}

    except Exception as e:
        db.rollback()
        logging.error("Error processing file: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            logging.debug("Removing temporary file: %s", tmp_path)
            os.remove(tmp_path)
