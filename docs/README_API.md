# Evo-Memory Financial Services API

Production-ready FastAPI implementation of Evo-Memory for financial services use cases.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
python3 main.py
```

The server will start at `http://localhost:8000`

### 3. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 4. Test the API

**Test Business Logic (No Server Required):**
```bash
python3 scripts/test_api_endpoints.py
```

**Test HTTP API (Server Required):**
```bash
# Terminal 1: Start server
python3 main.py

# Terminal 2: Run tests
python3 scripts/test_api_server.py
```

## 🏗️ Project Structure

```
evo_memory_poc/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints.py      # API route handlers
│   ├── core/
│   │   └── config.py              # Configuration
│   ├── models/
│   │   ├── memory.py             # Memory data models
│   │   ├── requests.py            # Request models
│   │   └── responses.py           # Response models
│   ├── services/
│   │   ├── agent_service.py       # Core agent logic
│   │   ├── financial_service.py   # Financial use cases
│   │   ├── llm_service.py         # LLM integration
│   │   └── memory_service.py      # Vector memory search
│   ├── utils/
│   └── main.py                    # FastAPI app
├── main.py                        # Server entry point
├── scripts/                       # Scripts and tests
│   ├── setup.sh                  # Setup script
│   ├── test_api_endpoints.py     # Test business logic
│   └── test_api_server.py        # Test HTTP API
├── docs/                          # Documentation
│   ├── README_API.md             # This file
│   └── ARCHITECTURE.md           # Architecture documentation
├── data/                          # Data storage
│   ├── memory.json
│   └── financial_memory.json
└── requirements.txt               # Dependencies
```

## 🔄 Data Flow

```
HTTP Request
    ↓
app/api/v1/endpoints.py (Route Handler)
    ↓
app/services/financial_service.py (Business Logic)
    ↓
app/services/agent_service.py (Core Agent)
    ↓
app/services/memory_service.py (Search) + app/services/llm_service.py (Generate)
    ↓
app/models/memory.py (MemoryEntry)
    ↓
HTTP Response (Pydantic Model)
```

## 🎯 Key Components

### 1. API Layer (`app/api/v1/endpoints.py`)
- FastAPI route handlers
- Request validation (Pydantic)
- Response formatting
- Error handling

### 2. Service Layer (`app/services/`)
- **agent_service.py**: Core Search → Synthesize → Evolve loop
- **financial_service.py**: Financial use cases (Risk, Compliance, Fraud, Portfolio)
- **llm_service.py**: LLM integration with OpenAI/Anthropic/Mock
- **memory_service.py**: Vector-based semantic search

### 3. Model Layer (`app/models/`)
- **memory.py**: MemoryEntry data class
- **requests.py**: Request validation models
- **responses.py**: Response models

### 4. Configuration (`app/core/config.py`)
- Environment variables
- LLM settings
- Vector search settings
- File paths
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
python3 main.py
```

The server will start at `http://localhost:8000`

### 3. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### Health Check
```bash
GET /api/v1/health
```

### General Task Solving
```bash
POST /api/v1/solve
Content-Type: application/json

{
  "task": "Solve: 2x² + 3x - 1 = 0",
  "task_type": "math",
  "use_llm": true
}
```

### Risk Assessment
```bash
POST /api/v1/risk
Content-Type: application/json

{
  "transaction_type": "Wire Transfer",
  "amount": 50000,
  "customer_tier": "NEW",
  "account_age_days": 15
}
```

### Compliance Check
```bash
POST /api/v1/compliance
Content-Type: application/json

{
  "transaction_type": "International Transfer",
  "amount": 15000,
  "region": "EU",
  "regulation": "AML"
}
```

### Fraud Detection
```bash
POST /api/v1/fraud
Content-Type: application/json

{
  "transaction_type": "Online Purchase",
  "amount": 5000,
  "customer_history": [
    {"amount": 100, "type": "purchase"},
    {"amount": 200, "type": "purchase"}
  ]
}
```

### Portfolio Optimization
```bash
POST /api/v1/portfolio
Content-Type: application/json

{
  "market_trend": "BULL",
  "volatility": "MEDIUM",
  "portfolio_value": 1000000,
  "current_allocation": "60/40"
}
```

### Statistics
```bash
GET /api/v1/stats
```

### Memory Retrieval
```bash
GET /api/v1/memories?limit=10&task_type=risk_assessment
```

## 📡 Example API Calls (cURL)

### Risk Assessment
```bash
curl -X POST "http://localhost:8000/api/v1/risk" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "Wire Transfer",
    "amount": 50000,
    "customer_tier": "NEW",
    "account_age_days": 15
  }'
```

### Compliance Check
```bash
curl -X POST "http://localhost:8000/api/v1/compliance" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "International Transfer",
    "amount": 15000,
    "region": "EU",
    "regulation": "AML"
  }'
```

### Fraud Detection
```bash
curl -X POST "http://localhost:8000/api/v1/fraud" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "Online Purchase",
    "amount": 5000,
    "customer_history": [
      {"amount": 100, "type": "purchase"},
      {"amount": 200, "type": "purchase"}
    ]
  }'
```

### Get Statistics
```bash
curl "http://localhost:8000/api/v1/stats"
```

## 🔧 Configuration

Set environment variables or edit `app/core/config.py`:

```bash
# LLM Configuration
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export LLM_PROVIDER="openai"  # or "anthropic"
export LLM_MODEL="gpt-4o-mini"

# Use mock LLM (no API key required)
export USE_MOCK_LLM="true"
```

## 🔧 Configuration

Set environment variables or edit `app/core/config.py`:

```bash
# LLM Configuration
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
export LLM_PROVIDER="openai"  # or "anthropic"
export LLM_MODEL="gpt-4o-mini"

# Use mock LLM (no API key required)
export USE_MOCK_LLM="true"
```

## 💡 Key Features

1. **Production-Ready Structure**: Clean separation of concerns
2. **Type Safety**: Pydantic models for request/response validation
3. **Vector Search**: Optional semantic search with FAISS
4. **LLM Integration**: Support for OpenAI and Anthropic
5. **Financial Use Cases**: Specialized endpoints for finance
6. **Memory Evolution**: Automatic learning from experience
7. **API Documentation**: Auto-generated Swagger/ReDoc

## 📊 Example Response

```json
{
  "task": "Assess risk for Wire Transfer transaction of $50,000.00...",
  "solution": "Risk Level: MEDIUM (Score: 55/100)...",
  "success": true,
  "context_used": 3,
  "memory_size": 15,
  "retrieved_experiences": [
    {
      "task": "Assess risk for...",
      "success": true,
      "task_type": "risk_assessment"
    }
  ]
}
```

## 🎯 Use Cases

- **Risk Assessment**: Learn from past risk decisions
- **Compliance**: Evolve understanding of regulations
- **Fraud Detection**: Improve detection patterns
- **Portfolio Optimization**: Refine strategies based on market conditions

## 📝 Notes

- Vector search requires `sentence-transformers` and `faiss-cpu`
- LLM integration requires API keys (or use mock mode)
- Memory is persisted to `data/memory.json` and `data/financial_memory.json`
- Vector index is stored in `data/memory_index.faiss`

