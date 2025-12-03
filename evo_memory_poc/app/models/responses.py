"""Response models for API."""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class TaskResponse(BaseModel):
    """Task solution response."""
    task: str
    solution: str
    success: bool
    context_used: int = Field(..., description="Number of past experiences used")
    memory_size: int = Field(..., description="Total number of memories")
    retrieved_experiences: List[Dict[str, Any]] = Field(default_factory=list, description="Retrieved experiences")


class StatsResponse(BaseModel):
    """Statistics response."""
    total_memories: int
    successful: int
    failed: int
    success_rate: float
    task_types: Dict[str, int]
    vector_index_size: int
    using_vector_search: bool


class MemoryListResponse(BaseModel):
    """Memory list response."""
    total: int
    returned: int
    memories: List[Dict[str, Any]]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    agent_ready: bool
    vector_search_available: bool
    llm_available: bool

