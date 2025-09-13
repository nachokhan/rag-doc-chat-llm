# mini-docufi

A minimal system that can:
1. Upload PDF/DOCX documents.
2. Parse them, store them, and generate embeddings per page and key “facts”.
3. Expose a conversation endpoint that can answer questions about the document, referencing pages and/or extracted facts.

## Requirements

- Python 3.11
- Docker and Docker Compose
- An OpenAI API Key

## Project Structure

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

## Local Setup (with venv)

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file by copying the example:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add your `OPENAI_API_KEY` and a `DATABASE_URL` for a local Postgres instance.

4. **Run database migrations:**
   You need a local Postgres server running with the pgvector extension enabled. Then run:
   ```bash
   alembic upgrade head
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Docker Setup

This is the recommended way to run the project.

1. **Set up environment variables:**
   Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add your `OPENAI_API_KEY`. The `DATABASE_URL` is already configured for the Docker network.

2. **Build and run with Makefile:**
   The `Makefile` provides convenient targets for managing the application.

   - **Build the containers:**
     ```bash
     make build
     ```

   - **Run database migrations:**
     ```bash
     make migrate
     ```

   - **Start the services in detached mode:**
     ```bash
     make run
     ```

   - **Stop the services:**
     ```bash
     make stop
     ```

   - **View logs:**
     ```bash
     make logs
     ```

   - **Run tests:**
     ```bash
     make test
     ```

## API Usage

The API will be available at `http://localhost:8000`.

### Upload a document

```bash
curl -X POST -F "file=@/path/to/your/document.pdf" http://localhost:8000/api/upload
```

**Response:**
```json
{
  "docId": "<your-document-id>"
}
```

### Converse with a document

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
  "docId": "<your-document-id>",
  "message": "What is this document about?"
}' \
http://localhost:8000/api/conversation
```

**Response:**
```json
{
  "reply": "The document is about...",
  "Sources": {
    "facts": [
      {
        "id": "...",
        "label": "...",
        "value_text": "...",
        "page": 1
      }
    ],
    "pages": [
      {
        "page": 1,
        "score": 0.84
      }
    ]
  }
}
```
