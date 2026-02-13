# Research Assistant RAG Application 🚀

A full-stack Retrieval-Augmented Generation (RAG) platform designed for academic research. This system enables researchers to fetch papers from ArXiv, store them in a hybrid database (PostgreSQL + ChromaDB), and interact with them through an AI-powered interface.

![Architecture](image.png)

## 🌟 Key Features

- **Automated Research**: Fetch and index academic papers directly from ArXiv.
- **Hybrid Storage**: Relational metadata in PostgreSQL paired with vector embeddings in ChromaDB.
- **Advanced RAG**: Semantic search and LLM-powered answering using LangChain.
- **Observability**: Integrated with Arize Phoenix for tracing and evaluation.
- **User Interface**: Intuitive Streamlit dashboard for research exploration.
- **Microservices Architecture**: Separate containers for API, UI, Vector Store, and Database.

## 🏗️ Architecture

The application follows a modular architecture designed for scalability:

1.  **FastAPI Backend**: Provides RESTful endpoints for RAG operations, knowledge graph queries, and data fetching.
2.  **Streamlit Frontend**: A responsive web interface for easy interaction with the research engine.
3.  **Data Persistence**: 
    - **PostgreSQL**: Stores structured metadata about articles and authors.
    - **ChromaDB**: Manages high-dimensional vector embeddings for semantic retrieval.
4.  **Observability Stack**: Uses OpenTelemetry and Arize Phoenix to trace LLM interactions and monitor system performance.

## 📁 Repository Structure

The project is organized into clear functional domains to ensure it remains easy to maintain as it grows.

```text
.
├── app/                  # Backend Service (FastAPI)
│   ├── api/routes/       # API endpoints and entry points
│   ├── core/             # Core business logic (RAG, KG, DB services)
│   ├── models/           # Pydantic data models for domain entities
│   ├── schemas/          # API request/response validation schemas
│   ├── prompts/          # LLM prompt templates and engineering
│   ├── utils/            # Helper functions and database drivers
│   └── main.py           # Application bootstrap
├── ui/                   # Frontend Service (Streamlit)
│   ├── ui.py             # Frontend application logic
│   └── Dockerfile        # Container configuration for the UI
├── init/                 # Database initialization and migration scripts
├── docker-compose.yml    # Service orchestration and environment setup
└── pyproject.toml        # Unified dependency management using UV
```

## 🚀 Getting Started

### Prerequisites

- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- An API Key for your preferred LLM provider (OpenAI, Mistral, etc.)

### Quick Start (Recommended)

Run the entire stack with a single command:

1. **Clone the repository**
2. **Setup Environment**: Create a `.env` file in the root directory.
3. **Launch**:
   ```bash
   docker-compose up --build
   ```
4. **Access**:
   - **Frontend UI**: `http://localhost:8501`
   - **Backend API Docs**: `http://localhost:8000/docs`
   - **Observability Hub**: `http://localhost:6006`

### Local Development

For active development, you can run services outside of Docker:

1. **Install dependencies**:
   ```bash
   pip install uv
   uv sync
   ```
2. **Start Backend**:
   ```bash
   uv run fastapi dev app/main.py
   ```
3. **Start Frontend**:
   ```bash
   streamlit run ui/ui.py
   ```

## 🔐 Configuration

Configuration is managed via environment variables. Key settings include:

- `OPENAI_API_KEY`: Your LLM provider key.
- `DATABASE_URL`: Connection string for PostgreSQL.
- `CHROMA_HOST` / `CHROMA_PORT`: Connection details for the vector store.

See `app/config.py` for a full list of available settings.

---

## 📜 Roadmap & Progress

- [x] Naive RAG Implementation
- [x] Observability Integration (Phoenix)
- [ ] Topic-based Metadata Filtering
- [ ] Multi-hop Retrieval & Reranking
- [ ] Automated Knowledge Graph Construction
- [ ] Comprehensive RAG Evaluation Framework