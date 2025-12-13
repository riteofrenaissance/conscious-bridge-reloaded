"""
Adaptation Manager - مدير التكيف
يدير تكيف النظام مع البيئة والمتغيرات
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from ..memory.memory_manager import memory_manager
from ..dialogue.dialogue_analyzer import dialogue_analyzer
from .evolution_engine import evolution_engine


class AdaptationStrategy(Enum):
    """استراتيجيات التكيف"""
    REACTIVE = "reactive"      # تفاعلي
    PROACTIVE = "proactive"    # استباقي
    PREDICTIVE = "predictive"  # تنبؤي
    TRANSFORMATIVE = "transformative"  # تحويلي


@dataclass
class AdaptationTrigger:
    """محفز التكيف"""
    id: str
    trigger_type: str
    description: str
    severity: float  # 0.0-1.0
    timestamp: datetime
    context: Dict[str, Any]
    resolved: bool = False
    resolution: Optional[str] = None


class AdaptationManager:
    """المدير الرئيسي للتكيف"""
    
    def __init__(self):
        self.adaptation_history: List[Dict] = []
        self.active_triggers: Dict[str, AdaptationTrigger] = {}
        self.current_strategy = AdaptationStrategy.REACTIVE
        self.adaptation_cooldown = timedelta(minutes=5)
        self.last_adaptation = None
        
        # أنماط التكيف المسبقة
        self.adaptation_patterns = {
            "high_error_rate": {
                "description": "معدل أخطاء مرتفع في الحوارات",
                "strategy": AdaptationStrategy.REACTIVE,
                "actions": ["زيادة الحذر في الردود", "التحقق المتكرر", "طلب التوضيح"]
            },
            "user_frustration": {
                "description": "إحباط متكرر من المستخدم",
                "strategy": AdaptationStrategy.PROACTIVE,
                "actions": ["تبسيط الردود", "زيادة التعاطف", "تقديم خيارات مساعدة"]
            },
            "knowledge_gap": {
                "description": "فجوة معرفية متكررة",
                "strategy": AdaptationStrategy.PREDICTIVE,
                "actions": ["توسيع قاعدة المعرفة", "تعلم مفاهيم جديدة", "تحسين البحث"]
            }
        }
    
    def monitor_system(self) -> List[str]:
        """مراقبة النظام واكتشاف محفزات التكيف"""
        triggers_activated = []
        
        # محاكاة اكتشاف محفزات
        mock_triggers = [
            {
                "type": "health_check",
                "description": "فحص صحة النظام الدوري",
                "severity": 0.3,
                "context": {"check_type": "routine"}
            }
        ]
        
        for trigger_data in mock_triggers:
            trigger_id = f"adapt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            trigger = AdaptationTrigger(
                id=trigger_id,
                trigger_type=trigger_data["type"],
                description=trigger_data["description"],
                severity=trigger_data["severity"],
                timestamp=datetime.now(),
                context=trigger_data["context"]
            )
            
            self.active_triggers[trigger_id] = trigger
            triggers_activated.append(trigger_id)
        
        return triggers_activated
    
    def evaluate_triggers(self) -> List[Dict]:
        """تقييم المحفزات النشطة واتخاذ الإجراءات"""
        if not self.active_triggers:
            return []
        
        actions_taken = []
        
        # تقييم كل محفز
        for trigger_id, trigger in list(self.active_triggers.items()):
            if trigger.resolved:
                continue
            
            if trigger.severity >= 0.5:
                action_result = self._execute_adaptation(trigger)
                actions_taken.append(action_result)
                
                trigger.resolved = True
                trigger.resolution = f"تم تنفيذ الإجراء"
        
        return actions_taken
    
    def _execute_adaptation(self, trigger: AdaptationTrigger) -> Dict[str, Any]:
        """تنفيذ إجراء تكيفي"""
        pattern = self.adaptation_patterns.get(trigger.trigger_type)
        
        if pattern:
            action_result = {
                "action_type": "pattern_based_adaptation",
                "strategy": pattern["strategy"].value,
                "description": pattern["description"],
                "trigger": trigger.trigger_type,
                "severity": trigger.severity,
                "changes": pattern["actions"]
            }
        else:
            action_result = {
                "action_type": "general_adaptation",
                "strategy": self.current_strategy.value,
                "description": "تعديل عام استجابة للمحفز",
                "trigger": trigger.trigger_type,
                "severity": trigger.severity,
                "changes": ["تعديل معاملات الثقة", "ضبط حدود القرار"]
            }
        
        self.last_adaptation = datetime.now()
        
        self.adaptation_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "adaptation_executed",
            "action_result": action_result,
            "trigger_id": trigger.id
        })
        
        return action_result
    
    def get_adaptation_report(self, hours: int = 24) -> Dict[str, Any]:
        """تقرير التكيف لفترة محددة"""
        return {
            "period_hours": hours,
            "total_events": len(self.adaptation_history),
            "active_triggers": len([t for t in self.active_triggers.values() if not t.resolved]),
            "current_strategy": self.current_strategy.value,
            "adaptation_cooldown_active": False,
            "recommendations": ["الاستمرار في المراقبة الدورية"],
            "report_timestamp": datetime.now().isoformat()
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المدير"""
        return {
            "current_strategy": self.current_strategy.value,
            "active_triggers_count": len([t for t in self.active_triggers.values() if not t.resolved]),
            "total_triggers_created": len(self.active_triggers),
            "adaptation_history_count": len(self.adaptation_history),
            "last_adaptation_time": self.last_adaptation.isoformat() if self.last_adaptation else None
        }


# إنشاء مثيل عالمي لمدير التكيف
adaptation_manager = AdaptationManager()
