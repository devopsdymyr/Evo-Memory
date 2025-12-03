"""Memory data models."""
from dataclasses import dataclass, asdict
from typing import List, Dict
from datetime import datetime


@dataclass
class MemoryEntry:
    """Represents a single memory entry with experience."""
    task: str
    solution: str
    success: bool
    reasoning: str
    timestamp: str
    task_type: str
    key_insights: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryEntry':
        return cls(**data)
    
    def to_api_dict(self) -> Dict:
        """Convert to API response format."""
        return {
            "task": self.task,
            "solution": self.solution[:200] + "..." if len(self.solution) > 200 else self.solution,
            "success": self.success,
            "task_type": self.task_type,
            "timestamp": self.timestamp,
            "key_insights": self.key_insights
        }

