"""
Deep Memory System - نظام الذاكرة العميقة
نظام تخزين طويل المدى مع فهرسة دلالية
"""

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import hashlib
from collections import defaultdict


class MemoryType(Enum):
    """أنواع الذكريات"""
    EXPERIENCE = "experience"
    INSIGHT = "insight"
    TRANSFORMATION = "transformation"
    DIALOGUE = "dialogue"
    WISDOM = "wisdom"
    CONSOLIDATED = "consolidated"


@dataclass
class MemoryEntry:
    """بنية دخول الذاكرة"""
    id: str
    content: Dict[str, Any]
    memory_type: MemoryType
    significance: float
    priority: int
    timestamp: datetime
    tags: Set[str] = field(default_factory=set)
    connections: Set[str] = field(default_factory=set)
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """تحويل إلى قاموس"""
        return {
            "id": self.id,
            "type": self.memory_type.value,
            "significance": self.significance,
            "timestamp": self.timestamp.isoformat(),
            "tags": list(self.tags),
            "access_count": self.access_count
        }


class DeepMemory:
    """نظام الذاكرة العميقة الرئيسي"""
    
    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self.memories: Dict[str, MemoryEntry] = {}
        self.tag_index: Dict[str, Set[str]] = defaultdict(set)
        self.type_index: Dict[MemoryType, Set[str]] = defaultdict(set)
        
    def store(self, content: Dict, memory_type: MemoryType, 
              significance: float = 0.5, tags: List[str] = None) -> str:
        """تخزين ذاكرة جديدة"""
        if tags is None:
            tags = []
        
        # توليد معرف فريد
        content_str = json.dumps(content, sort_keys=True)
        memory_id = f"mem_{hashlib.sha256(content_str.encode()).hexdigest()[:16]}"
        
        # إنشاء دخول الذاكرة
        memory = MemoryEntry(
            id=memory_id,
            content=content,
            memory_type=memory_type,
            significance=significance,
            priority=1,
            timestamp=datetime.now(),
            tags=set(tags)
        )
        
        # التخزين والفهرسة
        self.memories[memory_id] = memory
        for tag in tags:
            self.tag_index[tag].add(memory_id)
        self.type_index[memory_type].add(memory_id)
        
        return memory_id
    
    def search_by_tags(self, tags: List[str]) -> List[MemoryEntry]:
        """البحث بالوسوم"""
        if not tags:
            return []
        
        result_ids = set()
        for tag in tags:
            if tag in self.tag_index:
                result_ids.update(self.tag_index[tag])
        
        results = []
        for mem_id in result_ids:
            if mem_id in self.memories:
                memory = self.memories[mem_id]
                memory.access_count += 1
                memory.last_accessed = datetime.now()
                results.append(memory)
        
        return sorted(results, key=lambda x: x.significance, reverse=True)
    
    def get_statistics(self) -> Dict:
        """الحصول على إحصائيات النظام"""
        total = len(self.memories)
        if total == 0:
            return {"total_memories": 0, "status": "empty"}
        
        # توزيع الأنواع
        type_dist = {t.value: len(self.type_index[t]) for t in MemoryType}
        
        # حساب متوسط الأهمية
        significances = [m.significance for m in self.memories.values()]
        avg_significance = sum(significances) / len(significances)
        
        return {
            "total_memories": total,
            "capacity_usage": (total / self.capacity) * 100,
            "type_distribution": type_dist,
            "average_significance": round(avg_significance, 3),
            "unique_tags": len(self.tag_index)
        }


# إنشاء مثيل عالمي للذاكرة
memory_system = DeepMemory()

