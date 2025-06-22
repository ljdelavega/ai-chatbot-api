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

| Variable | Description | Default | Required | Notes |
|----------|-------------|---------|----------|-------|
| `API_KEY` | Client authentication key | `test-api-key` | ✅ | Used in X-API-Key header |
| `MODEL_PROVIDER` | AI provider (`gemini`) | `gemini` | ✅ | Currently supports Gemini |
| `MODEL_API_KEY` | Provider API key | `test-model-key` | ✅ | **Set to real key for production** |
| `ALLOWED_ORIGINS` | CORS origins (JSON array) | `["*"]` | No | Restrict for production |
| `LOG_LEVEL` | Logging level | `INFO` | No | DEBUG, INFO, WARNING, ERROR |

### 🔧 Configuration Modes

#### Test Mode (Default)
```env
API_KEY=test-api-key
MODEL_API_KEY=test-model-key  # Triggers mock responses
```

#### Production Mode
```env
API_KEY=your_secure_api_key_here
MODEL_API_KEY=your_actual_gemini_api_key  # Real Gemini API key
MODEL_PROVIDER=gemini
ALLOWED_ORIGINS=["https://yourdomain.com"]
LOG_LEVEL=INFO
```

**⚠️ Important**: 
- Set `MODEL_API_KEY` to your real Gemini API key to get actual AI responses
- Use `test-model-key` for development/testing with mock responses
- Always use a secure `API_KEY` in production (not `test-api-key`)

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
# Health check (no authentication required)
curl http://localhost:8000/api/v1/health

# Chat with correct API key (should succeed)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_secure_api_key_here" \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'

# Chat streaming with correct API key
curl -X POST http://localhost:8000/api/v1/chat/stream \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_secure_api_key_here" \
  -d '{"messages":[{"role":"user","content":"Count to 5"}]}'

# Test authentication failures
# Missing API key (should return 401)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'

# Wrong API key (should return 403)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: wrong-key" \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'

# Empty API key (should return 401)
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: " \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'
```

### PowerShell Testing Commands

```powershell
# Test with correct API key
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat" -Method Post -Headers @{ "Content-Type" = "application/json"; "X-API-Key" = "your_secure_api_key_here" } -Body '{ "messages": [ { "role": "user", "content": "Hello!" } ] }'

# Test authentication failures (use try-catch to handle errors)
try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat" -Method Post -Headers @{ "Content-Type" = "application/json"; "X-API-Key" = "wrong-key" } -Body '{ "messages": [ { "role": "user", "content": "test" } ] }'
} catch {
    Write-Host "Expected error: $($_.Exception.Message)"
}
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

- **API Key Authentication**: X-API-Key header validation with proper error handling
  - ✅ **401 Unauthorized**: Missing API key
  - ✅ **403 Forbidden**: Invalid API key
  - ✅ **200 Success**: Valid API key with real AI responses
- **CORS Protection**: Configurable allowed origins
- **Input Validation**: Pydantic models with strict validation
- **Container Security**: Non-root user, minimal attack surface
- **Error Handling**: Structured errors without information leakage
- **Environment Separation**: Test mode vs Production mode with different API keys

### 🔐 Authentication Flow

1. **Client Request**: Must include `X-API-Key: your_secure_api_key_here` header
2. **API Validation**: Compares against `API_KEY` environment variable
3. **AI Service Access**: Only calls Gemini API with valid authentication
4. **Error Responses**: Clear, structured error messages for debugging

**Security Best Practices:**
- Use strong, unique API keys in production
- Restrict CORS origins to your domain
- Monitor authentication failures in logs
- Rotate API keys regularly

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