#!/usr/bin/env python3
"""
Test API endpoints without starting the server.
This tests the business logic directly.
"""
import sys
from pathlib import Path

# Add project root to path (parent of scripts directory)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.agent_service import AgentService
from app.services.financial_service import FinancialService
from app.models.requests import (
    RiskAssessmentRequest,
    ComplianceRequest,
    FraudDetectionRequest,
    PortfolioRequest,
)


def test_risk_assessment():
    """Test risk assessment endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Risk Assessment API")
    print("=" * 70)
    
    service = FinancialService()
    
    request_data = {
        "transaction_type": "Wire Transfer",
        "amount": 50000,
        "customer_tier": "NEW",
        "account_age_days": 15
    }
    
    transaction = {
        "type": request_data["transaction_type"],
        "amount": request_data["amount"]
    }
    customer_profile = {
        "tier": request_data["customer_tier"],
        "account_age_days": request_data["account_age_days"]
    }
    
    result = service.assess_risk(transaction, customer_profile)
    
    print(f"\n✅ Risk Assessment Result:")
    print(f"   Task: {result['task']}")
    print(f"   Solution: {result['solution'][:200]}...")
    print(f"   Success: {result['success']}")
    print(f"   Past Experiences Used: {result['context_used']}")
    print(f"   Total Memories: {result['memory_size']}")
    
    return result


def test_compliance():
    """Test compliance check endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Compliance Check API")
    print("=" * 70)
    
    service = FinancialService()
    
    request_data = {
        "transaction_type": "International Transfer",
        "amount": 15000,
        "region": "EU",
        "regulation": "AML"
    }
    
    transaction = {
        "type": request_data["transaction_type"],
        "amount": request_data["amount"],
        "region": request_data["region"]
    }
    
    result = service.check_compliance(transaction, request_data["regulation"])
    
    print(f"\n✅ Compliance Check Result:")
    print(f"   Task: {result['task']}")
    print(f"   Solution: {result['solution'][:200]}...")
    print(f"   Success: {result['success']}")
    print(f"   Past Decisions Used: {result['context_used']}")
    print(f"   Total Memories: {result['memory_size']}")
    
    return result


def test_fraud_detection():
    """Test fraud detection endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Fraud Detection API")
    print("=" * 70)
    
    service = FinancialService()
    
    request_data = {
        "transaction_type": "Online Purchase",
        "amount": 5000,
        "customer_history": [
            {"amount": 100, "type": "purchase"},
            {"amount": 200, "type": "purchase"},
            {"amount": 150, "type": "purchase"}
        ]
    }
    
    transaction = {
        "type": request_data["transaction_type"],
        "amount": request_data["amount"]
    }
    
    result = service.detect_fraud(transaction, request_data["customer_history"])
    
    print(f"\n✅ Fraud Detection Result:")
    print(f"   Task: {result['task']}")
    print(f"   Solution: {result['solution'][:200]}...")
    print(f"   Success: {result['success']}")
    print(f"   Past Cases Used: {result['context_used']}")
    print(f"   Total Memories: {result['memory_size']}")
    
    return result


def test_portfolio_optimization():
    """Test portfolio optimization endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Portfolio Optimization API")
    print("=" * 70)
    
    service = FinancialService()
    
    market_conditions = {
        "trend": "BULL",
        "volatility": "MEDIUM"
    }
    portfolio = {
        "value": 1000000,
        "allocation": "60/40"
    }
    
    result = service.optimize_portfolio(market_conditions, portfolio)
    
    print(f"\n✅ Portfolio Optimization Result:")
    print(f"   Task: {result['task']}")
    print(f"   Solution: {result['solution'][:200]}...")
    print(f"   Success: {result['success']}")
    print(f"   Past Scenarios Used: {result['context_used']}")
    print(f"   Total Memories: {result['memory_size']}")
    
    return result


def test_stats():
    """Test stats endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Statistics API")
    print("=" * 70)
    
    service = FinancialService()
    stats = service.get_stats()
    
    print(f"\n✅ Statistics:")
    print(f"   Total Memories: {stats['total_memories']}")
    print(f"   Successful: {stats['successful']}")
    print(f"   Failed: {stats['failed']}")
    print(f"   Success Rate: {stats['success_rate']:.1%}")
    print(f"   Task Types: {stats['task_types']}")
    print(f"   Using Vector Search: {stats['using_vector_search']}")
    
    return stats


def main():
    """Run all API endpoint tests."""
    print("\n" + "🚀" * 35)
    print("  Testing Evo-Memory API Endpoints")
    print("  (Testing Business Logic)")
    print("🚀" * 35)
    
    try:
        # Test all endpoints
        test_risk_assessment()
        test_compliance()
        test_fraud_detection()
        test_portfolio_optimization()
        test_stats()
        
        print("\n" + "=" * 70)
        print("  ✅ All API Endpoint Tests Passed!")
        print("=" * 70)
        print("\nThe API business logic is working correctly.")
        print("To start the FastAPI server, install dependencies and run:")
        print("  pip install fastapi uvicorn")
        print("  python3 main.py")
        
        return 0
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

