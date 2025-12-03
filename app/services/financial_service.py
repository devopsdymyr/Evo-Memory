"""Financial services specialized agent."""
from typing import Dict, Any, List
from app.services.agent_service import AgentService
from app.services.llm_service import LLMService
from app.services.memory_service import MemoryService
from app.core.config import FINANCIAL_MEMORY_FILE


class FinancialService(AgentService):
    """Specialized service for financial use cases."""
    
    def __init__(self):
        llm = LLMService()
        memory = MemoryService(memory_file=FINANCIAL_MEMORY_FILE)
        super().__init__(llm, memory)
    
    def assess_risk(self, transaction: Dict, customer_profile: Dict) -> Dict[str, Any]:
        """Assess transaction risk."""
        task = f"Assess risk for {transaction.get('type')} transaction of ${transaction.get('amount'):,.2f} from {customer_profile.get('tier')} customer (account age: {customer_profile.get('account_age_days')} days)"
        return self.solve_task(task, task_type="risk_assessment", use_llm=True)
    
    def check_compliance(self, transaction: Dict, regulation: str) -> Dict[str, Any]:
        """Check regulatory compliance."""
        task = f"Check {regulation} compliance for {transaction.get('type')} transaction of ${transaction.get('amount'):,.2f} in {transaction.get('region')}"
        return self.solve_task(task, task_type="compliance", use_llm=True)
    
    def detect_fraud(self, transaction: Dict, customer_history: List[Dict]) -> Dict[str, Any]:
        """Detect fraud patterns."""
        avg_amount = sum(t.get("amount", 0) for t in customer_history) / len(customer_history) if customer_history else 0
        task = f"Detect fraud in {transaction.get('type')} transaction of ${transaction.get('amount'):,.2f}. Customer has {len(customer_history)} past transactions with average ${avg_amount:,.2f}"
        return self.solve_task(task, task_type="fraud_detection", use_llm=True)
    
    def optimize_portfolio(self, market_conditions: Dict, portfolio: Dict) -> Dict[str, Any]:
        """Optimize portfolio strategy."""
        task = f"Optimize portfolio for {market_conditions.get('trend')} market with {market_conditions.get('volatility')} volatility. Portfolio value: ${portfolio.get('value'):,.2f}"
        return self.solve_task(task, task_type="portfolio_optimization", use_llm=True)

