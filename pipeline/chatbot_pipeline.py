"""
chatbot_pipeline.py

High-level pipeline combining:
- optional audio transcription (tools.voice)
- embedding generation (sentence-transformers or OpenAI)
- vector search (FAISS)
- LLM-driven answer composition (LangChain / OpenAI)
- DB logging (tools.db)
"""

import os
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from langchain import OpenAI  # or LangChain wrappers you prefer
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from tools import db as db_tools
from tools import voice as voice_tools

# NOTE: you can swap in OpenAI embeddings or sentence-transformers locally
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
LLM_NAME = os.environ.get("LLM_MODEL", None)  # e.g., 'gpt-4o-mini' or None for local LLM

class ChatbotPipeline:
    def __init__(self, docs=None):
        # load embedding model
        self.embed_model = SentenceTransformer(EMBEDDING_MODEL)
        # load or build FAISS index
        self.index = None
        self.faiss_store = None
        self.llm = None
        self._init_llm()
        if docs is not None:
            self.build_faiss(docs)
        else:
            # load from disk if exists
            pass

    def _init_llm(self):
        if LLM_NAME:
            self.llm = OpenAI(model_name=LLM_NAME, temperature=0.0, max_tokens=512)
        else:
            # fallback: small local LLM or direct prompt-based setup
            self.llm = None

    def build_faiss(self, docs: List[dict]):
        # docs: list of {"id":..., "text":..., "meta":...}
        texts = [d['text'] for d in docs]
        embeddings = self.embed_model.encode(texts, convert_to_numpy=True)
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        faiss.normalize_L2(embeddings)
        index.add(embeddings)
        self.index = index
        # You'll want to persist index & metadata mapping for production

    def retrieve(self, query: str, top_k:int=5):
        q_emb = self.embed_model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(q_emb)
        D, I = self.index.search(q_emb, top_k)
        # retrieve text by indices - implement metadata mapping
        return I[0].tolist()

    def chat(self, text_query: str, patient_id: Optional[int]=None):
        # 1) retrieve context
        idxs = self.retrieve(text_query, top_k=5)
        context_text = " ".join(["[context snippet id="+str(i)+"]" for i in idxs])
        prompt = f"""You are a medical assistant. Use the context to answer carefully. Always include a safety disclaimer and advise seeking a clinician for medical guidance.\n\nContext:\n{context_text}\n\nUser: {text_query}\nAssistant:"""
        if self.llm:
            resp = self.llm(prompt)
            answer = resp
        else:
            # fallback simple answer
            answer = "This is a prototype. Please consult a healthcare professional."
        # log conversation to DB
        try:
            db_tools.save_conversation(patient_id=patient_id, user_input=text_query, bot_response=answer)
        except Exception:
            pass
        return answer

    def chat_with_audio(self, audio_path_or_base64: str, patient_id: Optional[int]=None):
        # Use tools.voice to get transcription
        text = voice_tools.transcribe_audio(audio_path_or_base64)
        return self.chat(text, patient_id=patient_id)
