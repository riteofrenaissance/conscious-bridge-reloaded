"""
Deep Memory System
Long-term storage and pattern recognition
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class MemoryEntry:
    """An entry in deep memory"""
    id: str
    content: Dict
    type: str  # experience, insight, transformation, dialogue
    significance: float
    timestamp: datetime
    tags: List[str] = field(default_factory=list)
    connections: List[str] = field(default_factory=list)
    accessed_count: int = 0
    last_accessed: Optional[datetime] = None


class DeepMemory:
    """
    Deep Memory for long-term storage
    
    Features:
    - Long-term storage with indexing
    - Pattern recognition across memories
    - Semantic search capabilities
    - Memory decay and consolidation
    """
    
    def __init__(self):
        self.memories: Dict[str, MemoryEntry] = {}
        self.memory_index: Dict[str, List[str]] = {}  # tag -> memory_ids
        self.access_patterns: Dict[str, int] = {}
        
    def store(self, content: Dict, memory_type: str, significance: float = 0.5, tags: List[str] = None) -> str:
        """Store a new memory"""
        memory_id = f"memory_{len(self.memories) + 1}"
        
        entry = MemoryEntry(
            id=memory_id,
            content=content,
            type=memory_type,
            significance=significance,
            timestamp=datetime.now(),
            tags=tags or []
        )
        
        self.memories[memory_id] = entry
        
        # Update index
        for tag in entry.tags:
            if tag not in self.memory_index:
                self.memory_index[tag] = []
            self.memory_index[tag].append(memory_id)
        
        return memory_id
    
    def retrieve(self, memory_id: str) -> Optional[MemoryEntry]:
        """Retrieve a specific memory"""
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            memory.accessed_count += 1
            memory.last_accessed = datetime.now()
            return memory
        return None
    
    def search_by_tag(self, tag: str) -> List[MemoryEntry]:
        """Search memories by tag"""
        memory_ids = self.memory_index.get(tag, [])
        memories = []
        
        for memory_id in memory_ids:
            memory = self.retrieve(memory_id)
            if memory:
                memories.append(memory)
        
        # Sort by significance (descending)
        memories.sort(key=lambda x: x.significance, reverse=True)
        return memories
    
    def search_by_type(self, memory_type: str) -> List[MemoryEntry]:
        """Search memories by type"""
        memories = []
        
        for memory in self.memories.values():
            if memory.type == memory_type:
                memories.append(memory)
        
        # Sort by timestamp (newest first)
        memories.sort(key=lambda x: x.timestamp, reverse=True)
        return memories
    
    def find_patterns(self, min_occurrences: int = 2) -> Dict[str, List[str]]:
        """Find patterns across memories"""
        patterns = {}
        
        # Simple pattern detection based on tags
        tag_counts = {}
        
        for memory in self.memories.values():
            for tag in memory.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Find tags that occur frequently
        for tag, count in tag_counts.items():
            if count >= min_occurrences:
                patterns[tag] = self.memory_index.get(tag, [])
        
        return patterns
    
    def consolidate(self, days_old: int = 30, min_significance: float = 0.3):
        """Consolidate old or insignificant memories"""
        now = datetime.now()
        to_remove = []
        
        for memory_id, memory in self.memories.items():
            # Calculate age in days
            age_days = (now - memory.timestamp).days
            
            # Check if memory should be consolidated (forgotten)
            if age_days > days_old and memory.significance < min_significance:
                to_remove.append(memory_id)
        
        # Remove consolidated memories
        for memory_id in to_remove:
            self._remove_memory(memory_id)
        
        return len(to_remove)
    
    def _remove_memory(self, memory_id: str):
        """Remove a memory and update index"""
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            
            # Remove from index
            for tag in memory.tags:
                if tag in self.memory_index and memory_id in self.memory_index[tag]:
                    self.memory_index[tag].remove(memory_id)
            
            # Remove memory
            del self.memories[memory_id]
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        total_memories = len(self.memories)
        total_tags = len(self.memory_index)
        
        # Calculate average significance
        if total_memories > 0:
            avg_significance = sum(m.significance for m in self.memories.values()) / total_memories
        else:
            avg_significance = 0.0
        
        # Count by type
        type_counts = {}
        for memory in self.memories.values():
            type_counts[memory.type] = type_counts.get(memory.type, 0) + 1
        
        return {
            "total_memories": total_memories,
            "total_tags": total_tags,
            "average_significance": round(avg_significance, 3),
            "memory_types": type_counts,
            "most_accessed": self._get_most_accessed()
        }
    
    def _get_most_accessed(self) -> List[Dict]:
        """Get most frequently accessed memories"""
        memories_list = list(self.memories.values())
        memories_list.sort(key=lambda x: x.accessed_count, reverse=True)
        
        return [
            {
                "id": m.id,
                "type": m.type,
                "accessed_count": m.accessed_count,
                "significance": m.significance
            }
            for m in memories_list[:5]
        ]
    
    def save_to_file(self, filename: str):
        """Save memory to file"""
        data = {
            "memories": {
                mid: {
                    "content": m.content,
                    "type": m.type,
                    "significance": m.significance,
                    "timestamp": m.timestamp.isoformat(),
                    "tags": m.tags,
                    "connections": m.connections,
                    "accessed_count": m.accessed_count,
                    "last_accessed": m.last_accessed.isoformat() if m.last_accessed else None
                }
                for mid, m in self.memories.items()
            },
            "memory_index": self.memory_index
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filename: str):
        """Load memory from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.memories.clear()
        self.memory_index.clear()
        
        for mid, mem_data in data.get("memories", {}).items():
            memory = MemoryEntry(
                id=mid,
                content=mem_data["content"],
                type=mem_data["type"],
                significance=mem_data["significance"],
                timestamp=datetime.fromisoformat(mem_data["timestamp"]),
                tags=mem_data.get("tags", []),
                connections=mem_data.get("connections", []),
                accessed_count=mem_data.get("accessed_count", 0),
                last_accessed=datetime.fromisoformat(mem_data["last_accessed"]) if mem_data.get("last_accessed") else None
            )
            self.memories[mid] = memory
        
        self.memory_index = data.get("memory_index", {})
