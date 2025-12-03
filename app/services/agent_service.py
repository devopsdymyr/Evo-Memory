"""Evo-Memory Agent service - Core business logic."""
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.models.memory import MemoryEntry
from app.services.llm_service import LLMService
from app.services.memory_service import MemoryService
from app.core.config import MEMORY_FILE, TOP_K_RETRIEVAL


class AgentService:
    """
    Evo-Memory Agent Service implementing Search → Synthesize → Evolve loop.
    """
    
    def __init__(self, llm_service: LLMService = None, memory_service: MemoryService = None):
        self.llm = llm_service or LLMService()
        self.memory = memory_service or MemoryService()
    
    def solve_task(self, task: str, task_type: str = "general", use_llm: bool = True) -> Dict[str, Any]:
        """
        Solve a task using Search → Synthesize → Evolve loop.
        
        Args:
            task: Task description
            task_type: Type of task
            use_llm: Whether to use LLM for solution
        
        Returns:
            Dict with task, solution, success, and metadata
        """
        # Step 1: Search
        retrieved = self.memory.search(task, task_type, top_k=TOP_K_RETRIEVAL)
        
        # Step 2: Synthesize
        context = self._synthesize_context(task, retrieved)
        
        # Step 3: Solve
        if use_llm:
            system_prompt = f"""You are a financial services AI assistant specializing in {task_type}.
Use the provided context from past experiences to solve the current task accurately.
Focus on patterns, strategies, and lessons learned from past experiences."""
            solution = self.llm.generate(context, system_prompt, max_tokens=500)
        else:
            solution = self._simple_solve(task, retrieved)
        
        # Step 4: Evolve
        success = self._evaluate_solution(task, solution)
        reasoning = f"Based on {len(retrieved)} past experiences"
        insights = self._extract_insights(task, solution, retrieved)
        
        new_memory = MemoryEntry(
            task=task,
            solution=solution,
            success=success,
            reasoning=reasoning,
            timestamp=datetime.now().isoformat(),
            task_type=task_type,
            key_insights=insights
        )
        
        self.memory.add_memory(new_memory)
        
        return {
            "task": task,
            "solution": solution,
            "success": success,
            "context_used": len(retrieved),
            "memory_size": len(self.memory.memories),
            "retrieved_experiences": [
                {"task": m.task[:100], "success": m.success, "task_type": m.task_type}
                for m in retrieved
            ]
        }
    
    def _synthesize_context(self, task: str, retrieved: List[MemoryEntry]) -> str:
        """Synthesize context from retrieved memories."""
        if not retrieved:
            return f"Task: {task}\n\nNo relevant past experiences found."
        
        context = f"Task: {task}\n\n"
        context += "Relevant Past Experiences:\n"
        context += "=" * 50 + "\n"
        
        for i, memory in enumerate(retrieved, 1):
            status = "✅ SUCCESS" if memory.success else "❌ FAILURE"
            context += f"\nExperience {i} ({status}):\n"
            context += f"Task: {memory.task}\n"
            context += f"Solution: {memory.solution}\n"
            context += f"Reasoning: {memory.reasoning}\n"
            if memory.key_insights:
                context += f"Key Insights: {', '.join(memory.key_insights)}\n"
            context += "-" * 50 + "\n"
        
        context += "\nBased on these experiences, apply similar strategies to solve the current task.\n"
        return context
    
    def _simple_solve(self, task: str, retrieved: List[MemoryEntry]) -> str:
        """Simple solver fallback."""
        if retrieved:
            successful = [m for m in retrieved if m.success]
            if successful:
                insights = []
                for mem in successful:
                    insights.extend(mem.key_insights)
                return f"Solution based on past successes: {', '.join(set(insights))}"
        return "Attempting solution based on available information."
    
    def _evaluate_solution(self, task: str, solution: str) -> bool:
        """Evaluate solution success."""
        return len(solution) > 50 and "error" not in solution.lower()
    
    def _extract_insights(self, task: str, solution: str, retrieved: List[MemoryEntry]) -> List[str]:
        """Extract key insights."""
        insights = []
        task_lower = task.lower()
        
        if "risk" in task_lower:
            insights.append("Risk assessment pattern identified")
        if "fraud" in task_lower:
            insights.append("Fraud detection pattern learned")
        if "compliance" in task_lower:
            insights.append("Compliance pattern recognized")
        if "portfolio" in task_lower or "market" in task_lower:
            insights.append("Portfolio strategy pattern learned")
        
        if retrieved:
            insights.append(f"Learned from {len(retrieved)} past experiences")
        
        return insights
    
    def get_stats(self) -> Dict:
        """Get agent statistics."""
        return self.memory.get_stats()

