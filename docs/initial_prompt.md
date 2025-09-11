# Prompt

I want you to generate a complete project called **mini-docufi** with the following scope and level of detail:

## Goal
A minimal but professional system that can:
1. Upload PDF/DOCX documents.
2. Parse them, store them, and generate embeddings per page and key “facts”.
3. Expose a conversation endpoint that can answer questions about the document, referencing pages and/or extracted facts.

## Technical Requirements

### Language and frameworks
- Python 3.11  
- FastAPI for the REST API  
- SQLAlchemy + Alembic for the database  
- Postgres 15 + pgvector extension (for embeddings)  
- openai or sentence-transformers for embeddings  
- pymupdf for PDFs, python-docx for DOCX  
- pytest for testing  

### Endpoints

Endpoints must return proper HTTP status (400 bad input, 404 unknown docId, 5xx errors)

1. **POST /upload**  
   - Payload: `multipart/form-data (file)`  
   - Stores the document, parses it into pages, extracts facts with an LLM, generates embeddings, and saves everything in Postgres.  
   - Response: `{ "docId": "<uuid>" }`

2. **POST /conversation**  
   - Payload: `{ "docId": "<uuid>", "message": "string" }`  
   - Retrieves relevant embeddings from facts and pages, calls an LLM with the context, and returns a grounded answer.  
   - Response:  
     ```json
     {
       "reply": "text",
       "Sources": {
         "facts": [{"id":"...", "label":"Revenue", "value_text":"$123M","page":7}],
         "pages": [{"page":7,"score":0.84}]
       }
     }
     ```

### Data Model
Tables:
- documents  
- pages  
- facts  
- messages (optional)  

Include either a `schema.sql` file or Alembic migrations.

### CLI Scripts
Generate inside `scripts/`:
1. `init_db.py` → create the tables.  
2. `embed_doc.py <path>` → manually process and embed a document.  
3. `evals.py` → run sample QAs to measure relevancy.  

### Infrastructure
- **Dockerfile** for the service (FastAPI + Uvicorn).  
- **docker-compose.yml** including:
  - Postgres 15 with pgvector enabled.  
  - `api` service mounting the code and exposing port 8000.  
- **Makefile** with targets: `run`, `format`, `test`.  

### Project Structure
```
mini-docufi/
  app/
    main.py
    models.py
    db.py
    routes/
      upload.py
      conversation.py
    services/
      embeddings.py
      facts.py
      chat.py
    utils/
      parser_pdf.py
      parser_docx.py
  migrations/
  scripts/
    init_db.py
    embed_doc.py
    evals.py
  tests/
    test_upload.py
    test_conversation.py
  Dockerfile
  docker-compose.yml
  Makefile
  requirements.txt
  README.md
```

### Tests
- Unit test for `/upload` with a small mock PDF file.  
- Unit test for `/conversation` that checks it returns 200 and contains both `reply` and `Sources`.  

### README.md
Must include:
- Local setup instructions using **pip** and `requirements.txt`.  
- How to run with Docker.  
- Required environment variables (`OPENAI_API_KEY`, `DATABASE_URL`).  
- Example `curl` commands for `/upload` and `/conversation`.  
