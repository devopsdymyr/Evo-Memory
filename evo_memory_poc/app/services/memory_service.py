"""Memory service for vector-based semantic search."""
import json
from pathlib import Path
from typing import List, Dict, Optional

# Optional vector dependencies
try:
    import numpy as np
    import faiss
    from sentence_transformers import SentenceTransformer
    HAS_VECTOR_DEPS = True
except ImportError:
    HAS_VECTOR_DEPS = False
    np = None
    faiss = None
    SentenceTransformer = None

from app.models.memory import MemoryEntry
from app.core.config import (
    EMBEDDING_MODEL, VECTOR_DIM, FAISS_INDEX_PATH, MEMORY_FILE, TOP_K_RETRIEVAL
)


class MemoryService:
    """Vector-based memory service with semantic search."""
    
    def __init__(self, memory_file: Path = None, use_vector: bool = True):
        self.memory_file = memory_file or MEMORY_FILE
        self.use_vector = use_vector and HAS_VECTOR_DEPS
        self.memories: List[MemoryEntry] = []
        self.index = None
        self.encoder = None
        
        if self.use_vector:
            self._init_vector_search()
        
        self.load_memories()
    
    def _init_vector_search(self):
        """Initialize vector search components."""
        try:
            self.encoder = SentenceTransformer(EMBEDDING_MODEL)
            self._build_index()
        except Exception as e:
            print(f"⚠️  Vector search initialization failed: {e}")
            self.use_vector = False
    
    def _build_index(self):
        """Build or load FAISS index."""
        try:
            if FAISS_INDEX_PATH.exists():
                self.index = faiss.read_index(str(FAISS_INDEX_PATH))
            else:
                self.index = faiss.IndexFlatL2(VECTOR_DIM)
        except:
            self.index = faiss.IndexFlatL2(VECTOR_DIM)
    
    def _encode_text(self, text: str):
        """Encode text to vector embedding."""
        if not self.use_vector or not self.encoder:
            return None
        try:
            embedding = self.encoder.encode([text], convert_to_numpy=True)
            return embedding[0].astype('float32')
        except:
            return None
    
    def load_memories(self):
        """Load memories from file."""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.memories = [MemoryEntry.from_dict(entry) for entry in data]
                
                # Rebuild index if using vector search
                if self.use_vector and self.index:
                    self.index = faiss.IndexFlatL2(VECTOR_DIM)
                    for memory in self.memories:
                        text = f"{memory.task} {memory.solution} {' '.join(memory.key_insights)}"
                        embedding = self._encode_text(text)
                        if embedding is not None:
                            embedding = embedding.reshape(1, -1)
                            self.index.add(embedding)
                
                print(f"✅ Loaded {len(self.memories)} memories")
            else:
                self.memories = []
        except Exception as e:
            print(f"⚠️  Error loading memories: {e}")
            self.memories = []
    
    def save_memories(self):
        """Save memories to file."""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump([m.to_dict() for m in self.memories], f, indent=2)
            
            if self.use_vector and self.index:
                faiss.write_index(self.index, str(FAISS_INDEX_PATH))
        except Exception as e:
            print(f"⚠️  Error saving memories: {e}")
    
    def add_memory(self, memory: MemoryEntry):
        """Add memory entry."""
        self.memories.append(memory)
        
        if self.use_vector and self.index:
            text = f"{memory.task} {memory.solution} {' '.join(memory.key_insights)}"
            embedding = self._encode_text(text)
            if embedding is not None:
                embedding = embedding.reshape(1, -1)
                self.index.add(embedding)
        
        self.save_memories()
    
    def search(self, query: str, task_type: str = None, top_k: int = None, 
               filter_success: Optional[bool] = None) -> List[MemoryEntry]:
        """Search for relevant memories."""
        top_k = top_k or TOP_K_RETRIEVAL
        
        if len(self.memories) == 0:
            return []
        
        if self.use_vector and self.index and self.index.ntotal > 0:
            return self._vector_search(query, task_type, top_k, filter_success)
        else:
            return self._text_search(query, task_type, top_k, filter_success)
    
    def _vector_search(self, query: str, task_type: str, top_k: int, 
                      filter_success: Optional[bool]) -> List[MemoryEntry]:
        """Vector-based semantic search."""
        query_embedding = self._encode_text(query)
        if query_embedding is None:
            return self._text_search(query, task_type, top_k, filter_success)
        
        query_embedding = query_embedding.reshape(1, -1)
        k = min(top_k * 2, len(self.memories))
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx >= len(self.memories):
                continue
            
            memory = self.memories[idx]
            if task_type and memory.task_type != task_type:
                continue
            if filter_success is not None and memory.success != filter_success:
                continue
            
            results.append((dist, memory))
            if len(results) >= top_k:
                break
        
        results.sort(key=lambda x: x[0])
        return [m for _, m in results]
    
    def _text_search(self, query: str, task_type: str, top_k: int,
                    filter_success: Optional[bool]) -> List[MemoryEntry]:
        """Simple text-based search."""
        results = []
        query_lower = query.lower()
        
        for memory in self.memories:
            if task_type and memory.task_type != task_type:
                continue
            if filter_success is not None and memory.success != filter_success:
                continue
            
            score = 0
            if query_lower in memory.task.lower():
                score += 2
            if any(word in memory.task.lower() for word in query_lower.split()[:3]):
                score += 1
            if memory.success:
                score += 1
            
            if score > 0:
                results.append((score, memory))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in results[:top_k]]
    
    def get_stats(self) -> Dict:
        """Get memory statistics."""
        total = len(self.memories)
        successful = sum(1 for m in self.memories if m.success)
        task_types = {}
        for m in self.memories:
            task_types[m.task_type] = task_types.get(m.task_type, 0) + 1
        
        return {
            "total_memories": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": successful / total if total > 0 else 0,
            "task_types": task_types,
            "vector_index_size": self.index.ntotal if (self.index and self.use_vector) else 0,
            "using_vector_search": self.use_vector
        }

