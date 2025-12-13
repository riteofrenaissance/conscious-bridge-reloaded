"""
Memory Manager - مدير نظام الذاكرة الشامل
"""

from datetime import datetime
from pathlib import Path
from .deep_memory import memory_system
from .experience_store import experience_store
from .insight_tracker import insight_tracker
from .consolidation_engine import consolidation_engine


class MemoryManager:
    """المدير الرئيسي لنظام الذاكرة"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """تهيئة النظام"""
        self.start_time = datetime.now()
        self.interaction_count = 0
    
    def process_interaction(self, user_input: str, ai_response: str) -> Dict[str, Any]:
        """معالجة تفاعل وحفظه"""
        self.interaction_count += 1
        
        # تخزين التجربة
        exp_id = experience_store.store_interaction(
            user_input=user_input,
            ai_response=ai_response,
            emotion="neutral",
            significance=0.5
        )
        
        # استخلاص أفكار في بعض الحالات
        insights = []
        if self.interaction_count % 5 == 0:
            insight_id = insight_tracker.add_insight(
                content=f"تفاعل رقم {self.interaction_count}: {user_input[:50]}...",
                confidence=0.7,
                category="interaction_pattern"
            )
            insights.append(insight_id)
        
        return {
            "experience_stored": exp_id,
            "insights_extracted": insights,
            "interaction_count": self.interaction_count
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات النظام"""
        return {
            "uptime_hours": round((datetime.now() - self.start_time).total_seconds() / 3600, 2),
            "total_interactions": self.interaction_count,
            "memory_system": memory_system.get_statistics(),
            "experience_store": experience_store.get_experience_stats(),
            "insight_tracker": insight_tracker.get_statistics(),
            "consolidation_engine": consolidation_engine.get_statistics()
        }


# إنشاء مثيل عالمي لمدير الذاكرة
memory_manager = MemoryManager()
