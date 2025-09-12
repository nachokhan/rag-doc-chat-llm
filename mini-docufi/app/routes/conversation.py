from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.services import chat

router = APIRouter()

class ConversationRequest(BaseModel):
    docId: str
    message: str

@router.post("/conversation")
def conversation(request: ConversationRequest, db: Session = Depends(get_db)):
    """Handles a conversation message and returns a grounded answer."""
    try:
        response = chat.get_chat_response(db, request.docId, request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
