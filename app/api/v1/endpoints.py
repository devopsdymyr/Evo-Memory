"""API v1 endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Optional

from app.models.requests import (
    TaskRequest,
    RiskAssessmentRequest,
    ComplianceRequest,
    FraudDetectionRequest,
    PortfolioRequest,
)
from app.models.responses import (
    TaskResponse,
    StatsResponse,
    MemoryListResponse,
    HealthResponse,
)
from app.services.agent_service import AgentService
from app.services.financial_service import FinancialService
from app.services.memory_service import MemoryService
from app.core.config import MEMORY_FILE

router = APIRouter()

# Initialize services
agent_service = AgentService()
financial_service = FinancialService()
memory_service = MemoryService()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        from app.services.llm_service import LLMService
        from app.services.memory_service import MemoryService
        
        llm = LLMService()
        memory = MemoryService()
        
        return HealthResponse(
            status="healthy",
            agent_ready=True,
            vector_search_available=memory.use_vector,
            llm_available=llm.provider != "mock"
        )
    except Exception as e:
        return HealthResponse(
            status="degraded",
            agent_ready=False,
            vector_search_available=False,
            llm_available=False
        )


@router.post("/solve", response_model=TaskResponse)
async def solve_task(request: TaskRequest):
    """Solve a general task."""
    try:
        result = agent_service.solve_task(
            task=request.task,
            task_type=request.task_type,
            use_llm=request.use_llm
        )
        return TaskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/risk", response_model=TaskResponse)
async def assess_risk(request: RiskAssessmentRequest):
    """Assess transaction risk."""
    try:
        transaction = {
            "type": request.transaction_type,
            "amount": request.amount
        }
        customer_profile = {
            "tier": request.customer_tier,
            "account_age_days": request.account_age_days
        }
        
        result = financial_service.assess_risk(transaction, customer_profile)
        return TaskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compliance", response_model=TaskResponse)
async def check_compliance(request: ComplianceRequest):
    """Check regulatory compliance."""
    try:
        transaction = {
            "type": request.transaction_type,
            "amount": request.amount,
            "region": request.region
        }
        
        result = financial_service.check_compliance(transaction, request.regulation)
        return TaskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fraud", response_model=TaskResponse)
async def detect_fraud(request: FraudDetectionRequest):
    """Detect fraud patterns."""
    try:
        transaction = {
            "type": request.transaction_type,
            "amount": request.amount
        }
        
        result = financial_service.detect_fraud(transaction, request.customer_history)
        return TaskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portfolio", response_model=TaskResponse)
async def optimize_portfolio(request: PortfolioRequest):
    """Optimize portfolio strategy."""
    try:
        market_conditions = {
            "trend": request.market_trend,
            "volatility": request.volatility
        }
        portfolio = {
            "value": request.portfolio_value,
            "allocation": request.current_allocation
        }
        
        result = financial_service.optimize_portfolio(market_conditions, portfolio)
        return TaskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get agent statistics."""
    try:
        stats = agent_service.get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memories", response_model=MemoryListResponse)
async def get_memories(limit: int = 10, task_type: Optional[str] = None):
    """Get recent memories."""
    try:
        memories = memory_service.memories
        
        if task_type:
            memories = [m for m in memories if m.task_type == task_type]
        
        memories = memories[-limit:]
        
        return MemoryListResponse(
            total=len(memory_service.memories),
            returned=len(memories),
            memories=[m.to_api_dict() for m in memories]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

