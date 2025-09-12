from fastapi import FastAPI

from app.routes import conversation, upload

app = FastAPI(
    title="mini-docufi",
    description="A minimal document Q&A system.",
    version="0.1.0",
)

app.include_router(upload.router, prefix="/api")
app.include_router(conversation.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
