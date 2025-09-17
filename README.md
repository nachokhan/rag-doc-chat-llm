# mini-docufi

## Project Overview
mini-docufi is an AI-powered document analysis and conversational platform. It allows users to upload documents, engage in natural language conversations with the document content, and perform market analysis based on extracted information and external web search.

## Features
*   **Document Upload:** Securely upload PDF and DOCX documents for analysis.
*   **Conversational AI:** Interact with your documents using natural language queries.
*   **Market Analysis:** Extract key insights and perform market analysis from document content.
*   **Fact Extraction:** Automatically identify and extract relevant facts from documents.
*   **Source Attribution:** Trace information back to its original source within the document.

## Setup Frontend

- **Navigate to the UI directory:**
  ```bash
  cd ui
  ```

- **Install dependencies:**
  ```bash
  npm install
  ```

- **Run the development server:**
  ```bash
  npm start
  ```
  The application will be available at `http://localhost:3000`.

## Setup Backend

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

The API will be available at `http://localhost:8000`.

## API Documentation

### Upload a Document
Upload a PDF or DOCX document for processing.

`POST /api/upload`

**Request:**
`multipart/form-data` with a `file` field.

**Example:**
```bash
curl -X POST -F "file=@/path/to/your/document.pdf" http://localhost:8000/api/upload
```

**Response:**
```json
{
  "docId": "<your-document-id>"
}
```

### Converse with a Document
Engage in a conversational chat with the content of an uploaded document.

`POST /api/conversation`

**Request:**
`application/json`
```json
{
  "docId": "<your-document-id>",
  "message": "What is this document about?"
}
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

### Start Market Analysis
Initiates a background task to perform market analysis based on a query.

`POST /api/analysis/market`

**Request:**
`application/json`
```json
{
  "query": "Analysis of the Q3 2023 tech market trends"
}
```

**Response:**
```json
{
  "message": "Analysis started",
  "task_id": "<your-task-id>"
}
```

### Stream Market Analysis Results
Streams real-time progress and final results of a market analysis task.

`GET /api/analysis/stream/{task_id}`

**Response:**
Server-Sent Events (SSE)
*   **Event: `progress`**
    ```json
    {"event": "progress", "data": "Current progress update..."}
    ```
*   **Event: `complete`**
    ```json
    {"event": "complete", "data": "Final analysis report..."}
    ```
*   **Event: `error`**
    ```json
    {"event": "error", "data": "Analysis failed."}
    ```
