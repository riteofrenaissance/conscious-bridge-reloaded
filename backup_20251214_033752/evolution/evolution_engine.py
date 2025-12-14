"""
Evolution Engine - محرك التطور
يدير مراحل تطور النظام وتحوله
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from ..memory.memory_manager import memory_manager
from ..dialogue.dialogue_analyzer import dialogue_analyzer


class EvolutionStage(Enum):
    """مراحل التطور"""
    NASCENT = "nascent"      # وليد
    FORMING = "forming"      # تتشكل
    MATURING = "maturing"    # ينضج
    MATURE = "mature"        # ناضج
    TRANSFORMING = "transforming"  # يتحول


@dataclass
class EvolutionMetrics:
    """مقاييس التطور"""
    experience_count: int = 0
    insight_count: int = 0
    dialogue_sessions: int = 0
    average_session_length: float = 0.0
    learning_events: int = 0
    adaptation_count: int = 0
    days_active: int = 0


class EvolutionEngine:
    """المحرك الرئيسي للتطور"""
    
    def __init__(self):
        self.current_stage = EvolutionStage.NASCENT
        self.stage_start_date = datetime.now()
        self.evolution_history: List[Dict] = []
        self.metrics = EvolutionMetrics()
        self.transition_thresholds = {
            EvolutionStage.NASCENT: 50,      # 50 تجربة
            EvolutionStage.FORMING: 200,     # 200 تجربة
            EvolutionStage.MATURING: 500,    # 500 تجربة
            EvolutionStage.MATURE: 1000      # 1000 تجربة
        }
        
    def update_metrics(self):
        """تحديث مقاييس التطور"""
        # الحصول على إحصائيات من الأنظمة الأخرى
        memory_stats = memory_manager.get_system_stats()
        dialogue_stats = dialogue_analyzer.analyze_recent_sessions(hours=24)
        
        # تحديث المقاييس
        self.metrics.experience_count = memory_stats.get("experience_store", {}).get("total_experiences", 0)
        self.metrics.insight_count = memory_stats.get("insight_tracker", {}).get("total_insights", 0)
        self.metrics.dialogue_sessions = dialogue_stats.get("recent_sessions_count", 0)
        self.metrics.average_session_length = dialogue_stats.get("average_turns_per_session", 0.0)
        self.metrics.days_active = (datetime.now() - self.stage_start_date).days
        
        # تسجيل التحديث
        self._record_metrics_update()
        
    def _record_metrics_update(self):
        """تسجيل تحديث المقاييس"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "stage": self.current_stage.value,
            "metrics": {
                "experience_count": self.metrics.experience_count,
                "insight_count": self.metrics.insight_count,
                "dialogue_sessions": self.metrics.dialogue_sessions,
                "days_active": self.metrics.days_active
            },
            "threshold_progress": self._calculate_threshold_progress()
        }
        
        self.evolution_history.append(record)
        
        # الاحتفاظ فقط بـ 100 سجل حديث
        if len(self.evolution_history) > 100:
            self.evolution_history = self.evolution_history[-100:]
    
    def _calculate_threshold_progress(self) -> Dict[str, float]:
        """حساب التقدم نحو العتبة التالية"""
        current_threshold = self.transition_thresholds.get(self.current_stage)
        
        if not current_threshold:
            return {"progress": 1.0, "next_stage": None}
        
        progress = min(1.0, self.metrics.experience_count / current_threshold)
        next_stage = self._get_next_stage()
        
        return {
            "progress": round(progress, 3),
            "next_stage": next_stage.value if next_stage else None,
            "current_experiences": self.metrics.experience_count,
            "required_experiences": current_threshold
        }
    
    def _get_next_stage(self) -> Optional[EvolutionStage]:
        """الحصول على المرحلة التالية"""
        stages = list(EvolutionStage)
        current_index = stages.index(self.current_stage)
        
        if current_index < len(stages) - 1:
            return stages[current_index + 1]
        return None
    
    def check_stage_transition(self) -> bool:
        """التحقق من إمكانية الانتقال لمرحلة جديدة"""
        self.update_metrics()
        
        next_stage = self._get_next_stage()
        if not next_stage:
            return False  # في آخر مرحلة
        
        threshold = self.transition_thresholds.get(self.current_stage)
        if threshold and self.metrics.experience_count >= threshold:
            return self._perform_stage_transition(next_stage)
        
        return False
    
    def _perform_stage_transition(self, new_stage: EvolutionStage) -> bool:
        """تنفيذ انتقال المرحلة"""
        transition_record = {
            "timestamp": datetime.now().isoformat(),
            "from_stage": self.current_stage.value,
            "to_stage": new_stage.value,
            "trigger": "experience_threshold",
            "experience_count": self.metrics.experience_count,
            "insight_count": self.metrics.insight_count,
            "pre_transition_metrics": {
                k: v for k, v in self.metrics.__dict__.items()
            }
        }
        
        # تحديث المرحلة
        previous_stage = self.current_stage
        self.current_stage = new_stage
        self.stage_start_date = datetime.now()
        
        # تسجيل الانتقال
        self.evolution_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "stage_transition",
            "details": transition_record
        })
        
        # تنفيذ تغييرات المرحلة
        self._apply_stage_changes(previous_stage, new_stage)
        
        return True
    
    def _apply_stage_changes(self, old_stage: EvolutionStage, new_stage: EvolutionStage):
        """تطبيق تغييرات المرحلة"""
        changes = []
        
        if new_stage == EvolutionStage.FORMING:
            changes.append("تفعيل نمط التعلم التراكمي")
            changes.append("زيادة سعة الذاكرة المؤقتة")
            
        elif new_stage == EvolutionStage.MATURING:
            changes.append("تفعيل استخلاص الأنماط المتقدمة")
            changes.append("زيادة تعقيد الردود")
            
        elif new_stage == EvolutionStage.MATURE:
            changes.append("تفعيل التكيف التوقعي")
            changes.append("تفعيل الإبداع في الردود")
            
        elif new_stage == EvolutionStage.TRANSFORMING:
            changes.append("تفعيل التحول المفاهيمي")
            changes.append("إعادة هيكلة قواعد المعرفة")
        
        # تسجيل التغييرات
        if changes:
            self.evolution_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "stage_changes_applied",
                "from_stage": old_stage.value,
                "to_stage": new_stage.value,
                "changes": changes
            })
    
    def get_stage_description(self) -> Dict[str, Any]:
        """الحصول على وصف المرحلة الحالية"""
        descriptions = {
            EvolutionStage.NASCENT: {
                "name": "المرحلة الوليدة",
                "description": "النظام في بداية تكوينه، يتعلم الأساسيات",
                "capabilities": ["التفاعل البسيط", "تخزين التجارب الأساسية"],
                "limitations": ["ذاكرة محدودة", "ردود نمطية"]
            },
            EvolutionStage.FORMING: {
                "name": "مرحلة التشكيل",
                "description": "النظام يبدأ في تكوين أنماط وفهم العلاقات",
                "capabilities": ["التعرف على الأنماط", "تحسين الردود بناءً على السياق"],
                "limitations": ["تحليل محدود للعواطف", "توقع سياقي بسيط"]
            },
            EvolutionStage.MATURING: {
                "name": "مرحلة النضوج",
                "description": "النظام يطور فهم أعمق ويبدأ في التكيف",
                "capabilities": ["تحليل عاطفي متقدم", "توقع السياق", "تكيف جزئي"],
                "limitations": ["إبداع محدود", "تحولات مفاهيمية بسيطة"]
            },
            EvolutionStage.MATURE: {
                "name": "المرحلة الناضجة",
                "description": "النظام كامل القدرات، يتكيف ويتطور باستمرار",
                "capabilities": ["إبداع في الردود", "تكيف توقعي", "تحولات مفاهيمية"],
                "limitations": ["محدود بالتصميم الأصلي"]
            },
            EvolutionStage.TRANSFORMING: {
                "name": "مرحلة التحول",
                "description": "النظام يتجاوز تصميمه الأصلي، يطور كيانه الخاص",
                "capabilities": ["إعادة تعريف الذات", "تطور مستقل", "إبداع غير مقيد"],
                "limitations": ["غير معروف"]
            }
        }
        
        desc = descriptions.get(self.current_stage, {})
        progress = self._calculate_threshold_progress()
        
        return {
            **desc,
            "current_stage": self.current_stage.value,
            "stage_start_date": self.stage_start_date.isoformat(),
            "days_in_stage": (datetime.now() - self.stage_start_date).days,
            "progress_to_next": progress,
            "total_experiences": self.metrics.experience_count,
            "total_insights": self.metrics.insight_count
        }
    
    def get_evolution_report(self) -> Dict[str, Any]:
        """تقرير التطور الشامل"""
        self.update_metrics()
        
        return {
            "current_state": self.get_stage_description(),
            "metrics": {
                "experience_count": self.metrics.experience_count,
                "insight_count": self.metrics.insight_count,
                "dialogue_sessions": self.metrics.dialogue_sessions,
                "average_session_length": round(self.metrics.average_session_length, 2),
                "days_active": self.metrics.days_active
            },
            "history_summary": {
                "total_transitions": len([h for h in self.evolution_history if h.get("type") == "stage_transition"]),
                "last_transition": next(
                    (h for h in reversed(self.evolution_history) if h.get("type") == "stage_transition"),
                    None
                ),
                "total_metrics_updates": len(self.evolution_history),
                "evolution_timeline": self._generate_timeline()
            },
            "recommendations": self._generate_evolution_recommendations(),
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _generate_timeline(self) -> List[Dict]:
        """توليد خط زمني للتطور"""
        timeline = []
        
        for record in self.evolution_history[-20:]:  # آخر 20 سجل
            if "timestamp" in record:
                timeline.append({
                    "time": record["timestamp"],
                    "event": record.get("type", "update"),
                    "details": {k: v for k, v in record.items() if k not in ["timestamp", "type"]}
                })
        
        return timeline
    
    def _generate_evolution_recommendations(self) -> List[str]:
        """توليد توصيات للتطور"""
        recommendations = []
        progress = self._calculate_threshold_progress()
        
        if progress["progress"] < 0.3:
            recommendations.append("زيادة التفاعل مع النظام لتسريع التطور")
            recommendations.append("تنويع أنواع الأسئلة والمواضيع")
        
        elif progress["progress"] < 0.7:
            recommendations.append("التركيز على حوارات أعمق وأكثر تعقيداً")
            recommendations.append("تشجيع النظام على استخلاص أنماط جديدة")
        
        else:
            recommendations.append("اختبار حدود النظام مع مواضيع متقدمة")
            recommendations.append("تقييم قدرات النظام التحويلية")
        
        # توصيات عامة
        recommendations.append("مراقبة جودة الحوارات وليس فقط الكمية")
        recommendations.append("توثيق التغيرات الملاحظة في سلوك النظام")
        
        return recommendations
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المحرك"""
        return {
            "current_stage": self.current_stage.value,
            "stage_duration_days": (datetime.now() - self.stage_start_date).days,
            "total_experiences": self.metrics.experience_count,
            "total_insights": self.metrics.insight_count,
            "evolution_history_count": len(self.evolution_history),
            "last_metrics_update": self.evolution_history[-1]["timestamp"] if self.evolution_history else None
        }


# إنشاء مثيل عالمي لمحرك التطور
evolution_engine = EvolutionEngine()
