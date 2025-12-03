"""Request models for API."""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class TaskRequest(BaseModel):
    """General task request."""
    task: str = Field(..., description="Task description")
    task_type: str = Field(default="general", description="Type of task")
    use_llm: bool = Field(default=True, description="Use LLM for solution generation")


class RiskAssessmentRequest(BaseModel):
    """Risk assessment request."""
    transaction_type: str = Field(..., description="Type of transaction")
    amount: float = Field(..., description="Transaction amount", gt=0)
    customer_tier: str = Field(..., description="Customer tier (NEW, REGULAR, PREMIUM)")
    account_age_days: int = Field(..., description="Account age in days", ge=0)


class ComplianceRequest(BaseModel):
    """Compliance check request."""
    transaction_type: str = Field(..., description="Type of transaction")
    amount: float = Field(..., description="Transaction amount", ge=0)
    region: str = Field(..., description="Transaction region")
    regulation: str = Field(..., description="Regulation to check (AML, KYC, SOX, GDPR, MiFID)")


class FraudDetectionRequest(BaseModel):
    """Fraud detection request."""
    transaction_type: str = Field(..., description="Type of transaction")
    amount: float = Field(..., description="Transaction amount", gt=0)
    customer_history: List[Dict[str, Any]] = Field(..., description="Customer transaction history")


class PortfolioRequest(BaseModel):
    """Portfolio optimization request."""
    market_trend: str = Field(..., description="Market trend (BULL, BEAR, SIDEWAYS)")
    volatility: str = Field(..., description="Volatility level (LOW, MEDIUM, HIGH)")
    portfolio_value: float = Field(..., description="Portfolio value", gt=0)
    current_allocation: Optional[str] = Field(default="60/40", description="Current allocation (equity/bonds)")

