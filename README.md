# AI Chatbot API

A production-ready, containerized AI chat API with streaming support. Built with FastAPI, LangChain, and Docker for maximum portability and performance.

## 🚀 Features

- **Real-time Streaming**: Progressive response delivery
- **Model Agnostic**: Support for Gemini, OpenAI, Anthropic (configurable)
- **Production Ready**: Docker containerization, health checks, structured logging
- **Developer Friendly**: Test mode, auto-generated docs, comprehensive error handling
- **Cloud Portable**: Deploy anywhere - Vercel, AWS, Google Cloud, or any container platform

## ⚡ Quick Commands

```bash
# Start everything (recommended)
docker-compose up -d

# Test health
curl http://localhost:8000/api/v1/health

# Test chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key" \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'

# View docs (open in browser)
# http://localhost:8000/docs
```

## 🏃 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone and start
git clone <repository-url>
cd ai-chatbot-api
docker-compose up -d

# Test the API
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key" \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'
```

### Option 2: Local Development

```bash
# Setup
poetry install
poetry run uvicorn app.main:app --reload

# Test
curl http://localhost:8000/api/v1/health
```

### Option 3: Docker Container

```bash
# Build and run
docker build -t ai-chatbot-api .
docker run -p 8000:8000 ai-chatbot-api

# Test
curl http://localhost:8000/api/v1/health
```

## 📋 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEY` | API key for authentication | `test-api-key` | ✅ |
| `MODEL_PROVIDER` | AI provider (`gemini`) | `gemini` | ✅ |
| `MODEL_API_KEY` | Provider API key | `test-model-key` | ✅ |
| `ALLOWED_ORIGINS` | CORS origins (JSON array) | `["*"]` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

**Example `.env`:**
```env
API_KEY=your-secure-api-key
MODEL_PROVIDER=gemini
MODEL_API_KEY=your-gemini-api-key
ALLOWED_ORIGINS=["http://localhost:3000"]
LOG_LEVEL=INFO
```

## 🔌 API Endpoints

### `GET /api/v1/health`
Health check endpoint.

```bash
curl http://localhost:8000/api/v1/health
```

**Response:**
```json
{"status":"healthy","timestamp":"2025-06-22T05:05:17.602860","version":"0.1.0"}
```

### `POST /api/v1/chat`
Complete AI response.

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is FastAPI?"}
    ]
  }'
```

**Response:**
```json
{"content":"Hello! This is a test response...","model":"gemini-2.0-flash"}
```

### `POST /api/v1/chat/stream`
Streaming AI response.

```bash
curl -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key" \
  -d '{
    "messages": [
      {"role": "user", "content": "Tell me a story"}
    ]
  }'
```

**Response:** Real-time streamed text chunks.

### `GET /docs`
Interactive API documentation (Swagger UI).

```bash
# Open in browser
http://localhost:8000/docs
```

## 🧪 Testing

### Run Unit Tests
```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov=app

# Specific test file
poetry run pytest tests/test_ai_services.py -v
```

### Manual Testing Commands

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Chat (complete response)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key" \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'

# Chat (streaming response)
curl -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key" \
  -d '{"messages":[{"role":"user","content":"Count to 5"}]}'

# Test authentication (should return 401)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'
```

## 🐳 Docker Commands

### Development with Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build -d
```

### Production Docker
```bash
# Build optimized image
docker build -t ai-chatbot-api .

# Run with environment variables
docker run -d -p 8000:8000 \
  -e API_KEY=your-api-key \
  -e MODEL_API_KEY=your-model-key \
  --name ai-chatbot \
  ai-chatbot-api

# Check container health
docker ps
docker logs ai-chatbot

# Stop and remove container
docker stop ai-chatbot
docker rm ai-chatbot
```

## 🏗️ Project Structure

```
ai-chatbot-api/
├── app/
│   ├── api/                    # API routing layer
│   │   ├── auth.py            # Authentication middleware
│   │   ├── models.py          # Pydantic models
│   │   └── v1.py              # API endpoints
│   ├── services/              # Business logic layer
│   │   ├── ai_service.py      # Abstract AI interface
│   │   ├── gemini_service.py  # Gemini implementation
│   │   └── ai_factory.py      # Service factory
│   ├── core/                  # Configuration and utilities
│   │   ├── config.py          # Environment config
│   │   └── logging.py         # Logging setup
│   └── main.py               # FastAPI application
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── Dockerfile                 # Multi-stage container build
├── docker-compose.yml         # Local development setup
├── pyproject.toml            # Poetry configuration
└── poetry.lock               # Locked dependencies
```

## ⚡ Development Workflow

### Local Development
```bash
# Install dependencies
poetry install

# Run with hot reload
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
poetry run pytest

# Format code
poetry run black app tests

# Type checking
poetry run mypy app
```

### Docker Development
```bash
# Start development environment
docker-compose up -d

# Watch logs
docker-compose logs -f ai-chatbot-api

# Execute commands in container
docker-compose exec ai-chatbot-api bash

# Restart after code changes
docker-compose restart ai-chatbot-api
```

## 🔒 Security Features

- **API Key Authentication**: X-API-Key header validation
- **CORS Protection**: Configurable allowed origins
- **Input Validation**: Pydantic models with strict validation
- **Container Security**: Non-root user, minimal attack surface
- **Error Handling**: Structured errors without information leakage

## 📊 Monitoring & Health

### Health Checks
```bash
# Application health
curl http://localhost:8000/api/v1/health

# Docker container health
docker ps  # Shows health status

# Detailed container inspection
docker inspect ai-chatbot-api | grep -A5 Health
```

### Logging
- **Structured JSON logging** for production
- **Configurable log levels** via `LOG_LEVEL`
- **Request/response logging** with correlation IDs
- **Error tracking** with stack traces

## 🚀 Deployment

### Cloud Platforms
The API is containerized and can be deployed to:

- **Vercel**: Container deployment support
- **AWS Lambda**: Container image support
- **Google Cloud Run**: Serverless containers
- **Azure Container Instances**: Direct container deployment
- **Any Kubernetes cluster**: Standard container workload

### Environment Setup for Production
```bash
# Required environment variables
export API_KEY="your-production-api-key"
export MODEL_API_KEY="your-gemini-api-key"
export MODEL_PROVIDER="gemini"
export ALLOWED_ORIGINS='["https://yourdomain.com"]'
export LOG_LEVEL="INFO"
```

## 📈 Performance

- **Streaming Responses**: Real-time progressive delivery
- **Async Architecture**: Non-blocking I/O operations
- **Container Optimization**: Multi-stage builds for minimal size
- **Health Monitoring**: Built-in health checks
- **Horizontal Scaling**: Stateless design for cloud deployment


## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.