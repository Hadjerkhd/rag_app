# Research Assistant API

![Research Assistant API Architecture](image.png)

## Overview

The Research Assistant API is a powerful FastAPI-based service that provides Retrieval Augmented Generation (RAG) capabilities for academic research. It combines document indexing, vector search, and AI-powered question answering to help researchers efficiently explore and analyze scientific literature, particularly from arXiv.

### Key Features

- **Document Processing**: Upload and index PDF and text documents
- **Vector Search**: Semantic search using sentence transformers and ChromaDB
- **AI-Powered Q&A**: Ask questions about your indexed documents using LLM integration
- **ArXiv Integration**: Fetch and index academic papers directly from arXiv
- **PostgreSQL Storage**: Persistent storage for articles and metadata
- **RESTful API**: Clean, documented API endpoints with authentication

## Architecture

The application follows a modular architecture:

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration settings
├── api/
│   ├── main.py         # API router setup
│   ├── deps.py         # Dependencies (auth, etc.)
│   └── routes/
│       ├── rag.py      # RAG endpoints
│       └── data_fetcher.py  # ArXiv fetching endpoints
├── core/
│   ├── rag.py          # RAG core functionality
│   └── data_fetcher.py # ArXiv fetching logic
├── schemas/            # Pydantic models
├── utils/              # Database utilities and CRUD operations
└── prompts/            # LLM prompt templates
```

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Framework for developing applications with LLMs
- **ChromaDB**: Vector database for embeddings
- **PostgreSQL**: Relational database for metadata storage
- **Sentence Transformers**: Text embedding models
- **OpenAI/Mistral**: Large Language Models for generation
- **ArXiv API**: Academic paper fetching
- **Docker**: Containerization

## API Endpoints

### RAG Endpoints (`/rag`)

#### `POST /answer-question`
Answer questions based on indexed documents using RAG.

**Request Body:**
```json
{
  "question": "What are the main findings of the paper?"
}
```

**Response:**
```json
{
  "answer": "Based on the indexed documents...",
  "confidence": 0.85,
  "sources": ["doc1.pdf", "doc2.pdf"]
}
```

#### `POST /index-doc`
Upload and index a document (PDF or TXT) for future querying.

**Request:** Multipart file upload
**Response:** Number of text chunks indexed

### Data Fetcher Endpoints (`/data-fetcher`)

#### `POST /fetch-arxiv-articles`
Fetch academic papers from arXiv and automatically index them.

**Request Body:**
```json
{
  "query": "machine learning transformers",
  "max_results": 10,
  "sort_criterion": "relevance"
}
```

**Response:**
```json
{
  "fetched_articles": [
    {
      "title": "Paper Title",
      "summary": "Abstract...",
      "pdf_url": "https://arxiv.org/pdf/...",
      "published": "2024-01-01",
      "llm_summary": "AI-generated summary..."
    }
  ],
  "total_count": 10
}
```

## Prerequisites

- Python 3.10+
- Docker and Docker Compose
- PostgreSQL
- ChromaDB
- OpenAI/Mistral API access

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd research-assistant-api
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Build and run with Docker:
```bash
docker build -t research-assistant-api .
docker run -p 8000:8000 research-assistant-api
```

### Local Development

1. Install dependencies using uv:
```bash
pip install uv
uv sync
```

2. Set up environment variables in `.env`:
```env
OPENAI_API_BASE=https://lab.iaparc.chapsvision.com/llm-gateway/
OPENAI_MODEL=Mistral-Small
OPENAI_API_KEY=your-api-key
CHROMA_DB_HOST=localhost
CHROMA_DB_PORT=8001
PG_DB_HOST=localhost
PG_DB_PORT=5433
PG_DB_NAME=researcher_assistantdb
PG_DB_USER_NAME=appuser
PG_password=apppassword
```

3. Start the development server:
```bash
make run-fastapi-dev
# or
uv run fastapi dev app/main.py
```

## Database Setup

The application uses PostgreSQL for storing article metadata. Initialize the database:

```sql
-- Run the initialization script
psql -f init/init.sql
```

The application will automatically create necessary tables on startup.

## Configuration

Key configuration options in `app/config.py`:

- **LLM Settings**: API base URL, model name, API key
- **Database**: PostgreSQL connection settings
- **Vector Store**: ChromaDB host and port
- **Authentication**: Token-based authentication

## Usage Examples

### 1. Index a Research Paper

```bash
curl -X POST "http://localhost:8000/index-doc" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@research_paper.pdf"
```

### 2. Ask Questions About Indexed Documents

```bash
curl -X POST "http://localhost:8000/answer-question" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "What methodology was used in the experiments?"}'
```

### 3. Fetch ArXiv Papers

```bash
curl -X POST "http://localhost:8000/fetch-arxiv-articles" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "attention mechanisms neural networks",
    "max_results": 5,
    "sort_criterion": "submittedDate"
  }'
```

## API Documentation

Once the server is running, visit:
- Interactive API docs: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Development

### Project Structure

- **Core Logic**: Business logic in `app/core/`
- **API Routes**: HTTP endpoints in `app/api/routes/`
- **Data Models**: Pydantic schemas in `app/schemas/`
- **Database**: SQLAlchemy models and CRUD in `app/utils/`
- **Configuration**: Environment-based config in `app/config.py`

### Adding New Features

1. Define Pydantic schemas in `app/schemas/`
2. Implement core logic in `app/core/`
3. Create API routes in `app/api/routes/`
4. Add database models/CRUD if needed
5. Update documentation

## Authentication

The API uses token-based authentication. Include the token in requests:

```bash
# Header format
Authorization: Bearer YOUR_JWT_TOKEN
```

## Error Handling

The API returns standard HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input)
- `401`: Unauthorized (missing/invalid token)
- `500`: Internal Server Error

## Performance Considerations

- **Vector Search**: ChromaDB provides efficient similarity search
- **Caching**: Consider implementing Redis for frequently accessed data
- **Async Operations**: Core functions use async/await for better performance
- **Database Indexing**: Ensure proper indexing on frequently queried fields

## Monitoring and Logging

- Application logs are written to stdout/stderr
- Database operations include error handling
- API responses include appropriate status codes and error messages

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions, please:
1. Check existing issues on GitHub
2. Create a new issue with detailed information
3. Provide reproduction steps for bugs
4. Include relevant logs and error messages

## Roadmap

- [ ] Support for more document formats (DOCX, HTML, etc.)
- [ ] Enhanced search with filtering and faceting
- [ ] Batch processing for multiple documents
- [ ] Citation tracking and reference extraction
- [ ] Integration with more academic databases
- [ ] Advanced analytics and usage metrics
- [ ] Multi-language support


