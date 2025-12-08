from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
from pipeline.chatbot_pipeline import ChatbotPipeline
from typing import Optional
import os

router = APIRouter()

# instantiate pipeline (singleton)
pipeline = ChatbotPipeline()

class ChatRequest(BaseModel):
    text: Optional[str] = None
    audio: Optional[str] = None  # optional path or base64

@router.post("/chat")
async def chat(req: ChatRequest):
    if not req.text and not req.audio:
        raise HTTPException(status_code=400, detail="Provide `text` or `audio`")
    # prefer audio if provided (assume pipeline handles it)
    if req.audio:
        reply = pipeline.chat_with_audio(req.audio)
    else:
        reply = pipeline.chat(req.text)
    return {"reply": reply}
