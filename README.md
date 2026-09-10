# Virtual-Medical-Care-Using-NLP

A reference implementation of an **interactive virtual medical chatbot** that accepts speech/text input, performs symptom understanding and retrieval over medical content, and produces conversational responses. This repo demonstrates an engineering prototype — **not** a certified medical device.

## Features
- Speech <> text pipeline (transcription & optional TTS)
- Semantic search with vector DB (FAISS) over symptom/illness database
- Conversational logic using LangChain/OpenAI-style LLMs (adapter)
- PostgreSQL-backed conversation history (patient linkage)
- Basic web UI (FastAPI) + REST endpoints for chat
- Safety & privacy recommendations included

## Important legal & safety note
This project is educational / research-oriented and **must not** be used in production for real medical diagnosis without clinical oversight, regulatory approval, and privacy compliance (HIPAA, GDPR, etc.). The assistant may produce incorrect or dangerous recommendations. Always route high-risk outcomes to licensed professionals and build explicit guardrails (human-in-loop, fallback, disclaimers, logging/alerting).

## Quickstart (local)
1. Copy your existing `db.py` and `voice.py` into `tools/` (or implement the provided stubs).
2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
