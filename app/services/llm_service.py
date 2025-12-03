"""LLM service for generating responses."""
from typing import Optional, Dict

# Optional imports
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    openai = None

try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    Anthropic = None

from app.core.config import (
    OPENAI_API_KEY, ANTHROPIC_API_KEY, LLM_PROVIDER, LLM_MODEL, USE_MOCK_LLM
)


class LLMService:
    """Unified LLM service supporting OpenAI and Anthropic."""
    
    def __init__(self, provider: str = None, model: str = None, use_mock: bool = None):
        self.provider = provider or LLM_PROVIDER
        self.model = model or LLM_MODEL
        self.use_mock = use_mock if use_mock is not None else USE_MOCK_LLM
        
        if self.use_mock:
            self.client = None
            self.provider = "mock"
        elif self.provider == "openai":
            if not HAS_OPENAI:
                raise ValueError("openai package not installed")
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set")
            self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        elif self.provider == "anthropic":
            if not HAS_ANTHROPIC:
                raise ValueError("anthropic package not installed")
            if not ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not set")
            self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        else:
            self.client = None
            self.provider = "mock"
    
    def generate(self, prompt: str, system_prompt: str = None, max_tokens: int = 500) -> str:
        """Generate response from LLM."""
        if self.use_mock or self.provider == "mock":
            return self._mock_generate(prompt)
        
        try:
            if self.provider == "openai":
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            elif self.provider == "anthropic":
                system_msg = system_prompt or ""
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    system=system_msg,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _mock_generate(self, prompt: str) -> str:
        """Generate mock response for testing."""
        prompt_lower = prompt.lower()
        
        if "risk" in prompt_lower:
            return """Risk Level: MEDIUM (Score: 55/100)

Reasoning: Based on the transaction amount ($50,000) and customer profile (NEW tier, 15 days old account), this transaction requires additional review. The high amount combined with a new customer account increases the risk profile. Similar past transactions with these characteristics have required manual review.

Recommendation: Flag for manual review before approval."""
        
        elif "fraud" in prompt_lower:
            return """Fraud Score: 65%

Analysis: This transaction shows unusual patterns compared to customer history. The amount ($5,000) is significantly higher than typical transactions (average $150). The transaction type (Online Purchase) combined with the amount deviation suggests potential fraud.

Action Required: Block transaction and notify fraud team for investigation."""
        
        elif "compliance" in prompt_lower or "aml" in prompt_lower:
            return """Compliance Status: REQUIRES_REVIEW

Analysis: This transaction exceeds the $10,000 threshold for automatic AML approval. The international transfer to EU region requires additional documentation per AML regulations. Based on past compliance decisions, similar transactions have required customer verification and source of funds documentation.

Required Actions:
1. Request customer verification documents
2. Collect source of funds information
3. Submit to compliance team for review"""
        
        elif "portfolio" in prompt_lower or "market" in prompt_lower:
            return """Recommended Strategy: Increase equity allocation to 70%, reduce bonds to 20%, maintain 10% cash reserves.

Expected Return: 8.5% based on current BULL market conditions and medium volatility.

Reasoning: Based on past market scenarios with similar conditions, increasing equity exposure during bull markets with medium volatility has historically provided optimal returns while maintaining acceptable risk levels."""
        
        else:
            return """Analysis complete. Based on past experiences and current context, this appears to be a standard case requiring standard procedures. The agent has learned from similar past experiences and applies the appropriate approach."""

