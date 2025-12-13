"""
Consolidation Engine - محرك دمج وتكثيف الذكريات
يدمج الذكريات المتشابهة في مفاهيم أعلى مستوى
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .deep_memory import memory_system, MemoryType, MemoryPriority


class MemoryCluster:
    """مجموعة ذكريات متشابهة"""
    
    def __init__(self, cluster_id: str, memory_ids: List[str]):
        self.id = cluster_id
        self.memory_ids = memory_ids
        self.created_at = datetime.now()
    
    def create_summary(self) -> Dict[str, Any]:
        """إنشاء ملخص للمجموعة"""
        return {
            "cluster_id": self.id,
            "memory_count": len(self.memory_ids),
            "created_at": self.created_at.isoformat()
        }


class ConsolidationEngine:
    """المحرك الرئيسي لدمج الذكريات"""
    
    def __init__(self):
        self.clusters: Dict[str, MemoryCluster] = {}
        self.consolidation_history: List[Dict] = []
        
    def create_consolidated_memory(self, memory_ids: List[str], summary: str) -> Optional[str]:
        """إنشاء ذاكرة موحدة من مجموعة ذكريات"""
        if len(memory_ids) < 2:
            return None
        
        # إنشاء محتوى موحد
        consolidated_content = {
            "type": "consolidated_memory",
            "component_memories": memory_ids,
            "summary": summary,
            "consolidation_timestamp": datetime.now().isoformat()
        }
        
        # تخزين في الذاكرة العميقة
        memory_id = memory_system.store(
            content=consolidated_content,
            memory_type=MemoryType.CONSOLIDATED,
            significance=0.8,  # أهمية عالية للذكريات الموحدة
            tags=["consolidated", "cluster"],
            priority=MemoryPriority.HIGH
        )
        
        # تسجيل العملية
        self.consolidation_history.append({
            "timestamp": datetime.now().isoformat(),
            "consolidated_memory_id": memory_id,
            "component_count": len(memory_ids),
            "summary": summary
        })
        
        return memory_id
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات الدمج"""
        return {
            "total_clusters": len(self.clusters),
            "total_consolidations": len(self.consolidation_history),
            "last_consolidation": self.consolidation_history[-1]["timestamp"] if self.consolidation_history else None
        }


# إنشاء مثيل عالمي لمحرك الدمج
consolidation_engine = ConsolidationEngine()
