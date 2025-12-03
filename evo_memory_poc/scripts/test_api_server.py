#!/usr/bin/env python3
"""
Test the FastAPI server with real HTTP requests.
This script tests all endpoints via HTTP.
"""
import requests
import json
import time
import sys
from pathlib import Path

# Add project root to path (for any future imports)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Health Check")
    print("=" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Health Check: {data['status']}")
        print(f"   Agent Ready: {data['agent_ready']}")
        print(f"   Vector Search: {data['vector_search_available']}")
        print(f"   LLM Available: {data['llm_available']}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with: python3 main.py")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_solve():
    """Test general solve endpoint."""
    print("\n" + "=" * 70)
    print("  Test: General Task Solving")
    print("=" * 70)
    
    payload = {
        "task": "Solve: 2x² + 3x - 1 = 0",
        "task_type": "math",
        "use_llm": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/solve", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Task Solved")
        print(f"   Task: {data['task']}")
        print(f"   Solution: {data['solution'][:150]}...")
        print(f"   Success: {data['success']}")
        print(f"   Experiences Used: {data['context_used']}")
        return True
    except Exception as e:
        print(f"❌ Solve failed: {e}")
        return False


def test_risk():
    """Test risk assessment endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Risk Assessment")
    print("=" * 70)
    
    payload = {
        "transaction_type": "Wire Transfer",
        "amount": 50000,
        "customer_tier": "NEW",
        "account_age_days": 15
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/risk", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Risk Assessed")
        print(f"   Task: {data['task']}")
        print(f"   Solution: {data['solution'][:150]}...")
        print(f"   Success: {data['success']}")
        print(f"   Past Cases Used: {data['context_used']}")
        return True
    except Exception as e:
        print(f"❌ Risk assessment failed: {e}")
        return False


def test_compliance():
    """Test compliance endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Compliance Check")
    print("=" * 70)
    
    payload = {
        "transaction_type": "International Transfer",
        "amount": 15000,
        "region": "EU",
        "regulation": "AML"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/compliance", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Compliance Checked")
        print(f"   Task: {data['task']}")
        print(f"   Solution: {data['solution'][:150]}...")
        print(f"   Success: {data['success']}")
        print(f"   Past Decisions Used: {data['context_used']}")
        return True
    except Exception as e:
        print(f"❌ Compliance check failed: {e}")
        return False


def test_fraud():
    """Test fraud detection endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Fraud Detection")
    print("=" * 70)
    
    payload = {
        "transaction_type": "Online Purchase",
        "amount": 5000,
        "customer_history": [
            {"amount": 100, "type": "purchase"},
            {"amount": 200, "type": "purchase"},
            {"amount": 150, "type": "purchase"}
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/fraud", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Fraud Detected")
        print(f"   Task: {data['task']}")
        print(f"   Solution: {data['solution'][:150]}...")
        print(f"   Success: {data['success']}")
        print(f"   Past Cases Used: {data['context_used']}")
        return True
    except Exception as e:
        print(f"❌ Fraud detection failed: {e}")
        return False


def test_portfolio():
    """Test portfolio optimization endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Portfolio Optimization")
    print("=" * 70)
    
    payload = {
        "market_trend": "BULL",
        "volatility": "MEDIUM",
        "portfolio_value": 1000000,
        "current_allocation": "60/40"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/portfolio", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Portfolio Optimized")
        print(f"   Task: {data['task']}")
        print(f"   Solution: {data['solution'][:150]}...")
        print(f"   Success: {data['success']}")
        print(f"   Past Scenarios Used: {data['context_used']}")
        return True
    except Exception as e:
        print(f"❌ Portfolio optimization failed: {e}")
        return False


def test_stats():
    """Test stats endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Statistics")
    print("=" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/stats", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Statistics Retrieved")
        print(f"   Total Memories: {data['total_memories']}")
        print(f"   Successful: {data['successful']}")
        print(f"   Failed: {data['failed']}")
        print(f"   Success Rate: {data['success_rate']:.1%}")
        print(f"   Task Types: {data['task_types']}")
        return True
    except Exception as e:
        print(f"❌ Stats failed: {e}")
        return False


def test_memories():
    """Test memories endpoint."""
    print("\n" + "=" * 70)
    print("  Test: Memory Retrieval")
    print("=" * 70)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/memories?limit=5", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Memories Retrieved")
        print(f"   Total: {data['total']}")
        print(f"   Returned: {data['returned']}")
        print(f"   Sample memories:")
        for i, mem in enumerate(data['memories'][:3], 1):
            print(f"      {i}. {mem['task'][:60]}...")
        return True
    except Exception as e:
        print(f"❌ Memories retrieval failed: {e}")
        return False


def main():
    """Run all API tests."""
    print("\n" + "🚀" * 35)
    print("  Testing Evo-Memory FastAPI Server")
    print("  (HTTP API Endpoints)")
    print("🚀" * 35)
    
    # Check if server is running
    if not test_health():
        print("\n⚠️  Please start the server first:")
        print("   python3 main.py")
        return 1
    
    results = []
    
    # Test all endpoints
    results.append(("Health", test_health()))
    results.append(("Solve", test_solve()))
    results.append(("Risk", test_risk()))
    results.append(("Compliance", test_compliance()))
    results.append(("Fraud", test_fraud()))
    results.append(("Portfolio", test_portfolio()))
    results.append(("Stats", test_stats()))
    results.append(("Memories", test_memories()))
    
    # Summary
    print("\n" + "=" * 70)
    print("  Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {name}: {status}")
    
    print(f"\n   Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All API tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

