"""Configuration for Evo-Memory POC."""
import os
from pathlib import Path

# Optional dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "true").lower() == "true"

# Vector Database
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTOR_DIM = 384
FAISS_INDEX_PATH = BASE_DIR / "data" / "memory_index.faiss"

# Memory Configuration
MEMORY_FILE = BASE_DIR / "data" / "memory.json"
FINANCIAL_MEMORY_FILE = BASE_DIR / "data" / "financial_memory.json"
MAX_MEMORY_ENTRIES = 1000
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "5"))

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_TITLE = "Evo-Memory Financial Services API"
API_VERSION = "1.0.0"
API_DESCRIPTION = """
Evo-Memory API for Financial Services - Experience Reuse in LLM Agents

This API demonstrates how AI agents can learn from experience for:
- Risk Assessment
- Compliance Checking
- Fraud Detection
- Portfolio Optimization
"""

# Financial Services Configuration
RISK_THRESHOLDS = {
    "LOW": 0,
    "MEDIUM": 40,
    "HIGH": 60,
    "CRITICAL": 80
}

COMPLIANCE_REGULATIONS = ["AML", "KYC", "SOX", "GDPR", "MiFID", "PCI-DSS"]

# Create data directory
(BASE_DIR / "data").mkdir(exist_ok=True)

