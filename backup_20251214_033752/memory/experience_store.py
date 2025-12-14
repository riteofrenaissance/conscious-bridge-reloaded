"""
Experience Store - مخزن التجارب التفاعلية
يخزن ويحلل التجارب التفاعلية مع المستخدمين
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from .deep_memory import memory_system, MemoryType, MemoryPriority


class ExperienceStore:
    """مخزن متخصص للتجارب التفاعلية"""
    
    def __init__(self):
        self.experience_counter = 0
        
    def store_interaction(self, 
                         user_input: str, 
                         ai_response: str,
                         context: Dict[str, Any] = None,
                         emotion: str = "neutral",
                         significance: float = 0.5,
                         tags: List[str] = None) -> str:
        """تخزين تجربة تفاعلية"""
        if tags is None:
            tags = []
        
        experience_data = {
            "type": "interaction",
            "user_input": user_input,
            "ai_response": ai_response,
            "context": context or {},
            "emotion": emotion,
            "timestamp": datetime.now().isoformat()
        }
        
        # إضافة وسوم تلقائية
        auto_tags = ["experience", "interaction", f"emotion_{emotion}"]
        if len(user_input.split()) > 10:
            auto_tags.append("detailed_input")
        
        all_tags = list(set(tags + auto_tags))
        
        # تحديد الأهمية بناءً على المحتوى
        if any(word in user_input.lower() for word in ["مهم", "ضروري", "حاسم"]):
            significance = max(significance, 0.8)
            priority = MemoryPriority.HIGH
        else:
            priority = MemoryPriority.MEDIUM
        
        # تخزين في الذاكرة العميقة
        memory_id = memory_system.store(
            content=experience_data,
            memory_type=MemoryType.EXPERIENCE,
            significance=significance,
            tags=all_tags,
            priority=priority
        )
        
        self.experience_counter += 1
        return memory_id
    
    def get_experience_stats(self) -> Dict[str, Any]:
        """الحصول على إحصائيات التجارب"""
        experiences = memory_system.search_by_tags(["experience"])
        
        if not experiences:
            return {"total_experiences": 0}
        
        return {
            "total_experiences": len(experiences),
            "average_significance": round(
                sum(exp.significance for exp in experiences) / len(experiences), 
                3
            )
        }


# إنشاء مثيل عالمي لمخزن التجارب
experience_store = ExperienceStore()
