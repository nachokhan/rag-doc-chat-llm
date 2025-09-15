# mini-docufi

## Setup

- **Set up environment variables:**
   Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add your `OPENAI_API_KEY`. The `DATABASE_URL` is already configured for the Docker network.

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
