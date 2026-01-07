# AeroAssist

AI-powered document search for manufacturing operations using RAG (Retrieval-Augmented Generation).

## What it does

Ask a question → Get the answer + source citation. Instantly.

Turns "let me check the manual" into real-time answers from technical documents.

## Tech Stack

- **Python**
- **LangChain** — RAG orchestration
- **ChromaDB** — Vector database
- **Cohere** — Embeddings & LLM
- **Streamlit** — Frontend

## How it works

1. Documents are chunked and embedded into a vector database
2. User asks a question
3. Semantic search finds relevant sections
4. LLM generates answer with source citations

## Setup

1. Clone the repo
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Add your API key to `.env`:
```
   COHERE_API_KEY=your_key_here
```
4. Run the app:
```bash
   streamlit run app.py
```
5, Screenshot

<img width="1024" height="535" alt="image" src="https://github.com/user-attachments/assets/93f2851b-1652-4209-93da-b3f590a2cf78" />

