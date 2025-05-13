# 🚀 Upstart AI – Startup Idea Evaluator Agent

Upstart AI is an intelligent, agent-like assistant that helps startup founders analyze, refine, and validate their business ideas using Large Language Models (LLMs), real-time market data, and semantic search.

---

## ✨ Features

- 🧠 **LLM-Powered Evaluation** – Uses GPT-4 to analyze your startup idea with structured insights:
  - Market overview
  - Target customer segments
  - Pain points solved
  - Revenue model
- 🌐 **Live Competitor Analysis** – Fetches real-time competitor data via SerpAPI (Google Search).
- 📚 **Document-Aware Feedback (RAG)** – Accepts PDF pitch decks and uses vector search to enhance LLM responses.
- 🧠 **Semantic Memory** – Compares your idea to previous sessions using FAISS + sentence-transformers.
- 📊 **Clear Structured Output** – Returns readable suggestions and context, ready for business planning or pitch refining.
- 🖥 **Streamlit UI** – Simple interactive interface with dark-themed landing screen and background video.

---

## 🛠 Tech Stack

- **LLMs**: OpenAI API (GPT-4 / GPT-3.5)
- **Semantic Search**: SentenceTransformers, FAISS
- **Web Search**: SerpAPI
- **Frontend**: Streamlit + Custom CSS
- **RAG**: Retrieval-Augmented Generation over logs + uploaded PDFs

---

## 🧪 Demo Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourname/upstart-ai.git
cd upstart-ai```

### 2. Install dependencies
bash

pip install -r requirements.tx
