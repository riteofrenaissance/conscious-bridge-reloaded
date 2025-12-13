"""
Insight Tracker - متتبع الأفكار والاستنتاجات
يتتبع الاستنتاجات المستخلصة من التجارب
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .deep_memory import memory_system, MemoryType, MemoryPriority


class Insight:
    """فكرة/استنتاج مستخلص"""
    
    def __init__(self, content: str, confidence: float, category: str = "general"):
        self.id = f"insight_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.content = content
        self.confidence = confidence
        self.category = category
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        """تحويل إلى قاموس"""
        return {
            "id": self.id,
            "content": self.content,
            "confidence": round(self.confidence, 3),
            "category": self.category,
            "timestamp": self.timestamp.isoformat()
        }


class InsightTracker:
    """المتتبع الرئيسي للأفكار"""
    
    def __init__(self):
        self.insights: Dict[str, Insight] = {}
        self.categories = set()
        
    def add_insight(self, content: str, confidence: float = 0.7, category: str = "general") -> str:
        """إضافة فكرة جديدة"""
        insight = Insight(content, confidence, category)
        
        # تخزين محلي
        self.insights[insight.id] = insight
        self.categories.add(category)
        
        # تخزين في الذاكرة العميقة
        insight_data = insight.to_dict()
        
        memory_system.store(
            content=insight_data,
            memory_type=MemoryType.INSIGHT,
            significance=confidence,
            tags=["insight", category],
            priority=MemoryPriority.HIGH if confidence > 0.8 else MemoryPriority.MEDIUM
        )
        
        return insight.id
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المتتبع"""
        total_insights = len(self.insights)
        
        if total_insights == 0:
            return {"total_insights": 0}
        
        # حساب متوسط الثقة
        avg_confidence = sum(i.confidence for i in self.insights.values()) / total_insights
        
        # توزيع التصنيفات
        category_dist = {}
        for insight in self.insights.values():
            category_dist[insight.category] = category_dist.get(insight.category, 0) + 1
        
        return {
            "total_insights": total_insights,
            "categories_count": len(self.categories),
            "average_confidence": round(avg_confidence, 3),
            "category_distribution": category_dist
        }


# إنشاء مثيل عالمي لمتتبع الأفكار
insight_tracker = InsightTracker()
