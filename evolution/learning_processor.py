"""
Learning Processor - معالج التعلم
يدير عمليات التعلم واكتساب المهارات
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum


class LearningType(Enum):
    """أنواع التعلم"""
    EXPERIENTIAL = "experiential"      # تعلم من التجارب
    PATTERN = "pattern"                # تعلم الأنماط
    CONCEPTUAL = "conceptual"          # تعلم المفاهيم
    ADAPTIVE = "adaptive"              # تعلم تكيفي


@dataclass
class LearningRecord:
    """سجل تعلم"""
    id: str
    learning_type: LearningType
    skill: str
    initial_proficiency: float  # 0.0-1.0
    final_proficiency: float    # 0.0-1.0
    improvement: float
    duration_minutes: int
    timestamp: datetime
    source_memories: List[str] = None
    confidence: float = 0.7
    
    def to_dict(self) -> Dict:
        """تحويل إلى قاموس"""
        return {
            "id": self.id,
            "learning_type": self.learning_type.value,
            "skill": self.skill,
            "initial_proficiency": round(self.initial_proficiency, 3),
            "final_proficiency": round(self.final_proficiency, 3),
            "improvement": round(self.improvement, 3),
            "duration_minutes": self.duration_minutes,
            "efficiency": round(self.improvement / max(self.duration_minutes, 1), 4),
            "timestamp": self.timestamp.isoformat(),
            "confidence": round(self.confidence, 3),
            "source_memories": self.source_memories or []
        }


class LearningProcessor:
    """المعالج الرئيسي للتعلم"""
    
    def __init__(self):
        self.learning_records: Dict[str, LearningRecord] = {}
        self.skill_proficiencies: Dict[str, float] = {}  # مهارة -> إتقان (0.0-1.0)
        self.learning_history: List[Dict] = []
        
        # المهارات الأساسية
        self.base_skills = {
            "dialogue_response": 0.3,
            "emotion_recognition": 0.2,
            "context_understanding": 0.4,
            "pattern_detection": 0.3,
            "memory_retrieval": 0.5
        }
        self.skill_proficiencies.update(self.base_skills)
    
    def process_learning(self, 
                        skill: str, 
                        learning_type: LearningType,
                        improvement_data: Dict[str, Any],
                        duration_minutes: int = 5,
                        source_memories: List[str] = None) -> Optional[str]:
        """معالجة حدث تعلم"""
        
        # الحصول على الإتقان الحالي
        current_proficiency = self.skill_proficiencies.get(skill, 0.0)
        
        # حساب التحسين
        improvement = self._calculate_improvement(learning_type, improvement_data, current_proficiency)
        
        if improvement <= 0:
            return None  # لا تحسين
        
        # تحديث الإتقان
        new_proficiency = min(1.0, current_proficiency + improvement)
        self.skill_proficiencies[skill] = new_proficiency
        
        # إنشاء سجل التعلم
        record_id = f"learn_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{skill[:10]}"
        
        record = LearningRecord(
            id=record_id,
            learning_type=learning_type,
            skill=skill,
            initial_proficiency=current_proficiency,
            final_proficiency=new_proficiency,
            improvement=improvement,
            duration_minutes=duration_minutes,
            timestamp=datetime.now(),
            source_memories=source_memories,
            confidence=self._calculate_confidence(learning_type, improvement_data)
        )
        
        # حفظ السجل
        self.learning_records[record_id] = record
        
        # تسجيل في التاريخ
        self.learning_history.append({
            "timestamp": datetime.now().isoformat(),
            "record_id": record_id,
            "skill": skill,
            "improvement": improvement,
            "new_proficiency": new_proficiency
        })
        
        # تطبيق تأثيرات التعلم
        self._apply_learning_effects(skill, improvement, learning_type)
        
        return record_id
    
    def _calculate_improvement(self, 
                              learning_type: LearningType,
                              data: Dict[str, Any],
                              current_proficiency: float) -> float:
        """حساب مقدار التحسين"""
        base_improvement = 0.05  # أساسي
        
        # تعديل حسب نوع التعلم
        type_multipliers = {
            LearningType.EXPERIENTIAL: 1.0,
            LearningType.PATTERN: 1.2,
            LearningType.CONCEPTUAL: 1.5,
            LearningType.ADAPTIVE: 2.0
        }
        
        multiplier = type_multipliers.get(learning_type, 1.0)
        
        # تعديل حسب جودة البيانات
        data_quality = data.get("quality", 0.5)
        quality_bonus = data_quality * 0.1
        
        # تعديل حسب التكرار
        repetition_count = data.get("repetition", 1)
        repetition_bonus = min(0.3, repetition_count * 0.05)
        
        # تقليل التحسين مع زيادة الإتقان
        proficiency_penalty = current_proficiency * 0.3
        
        # الحساب النهائي
        improvement = (base_improvement + quality_bonus + repetition_bonus) * multiplier
        improvement = max(0.01, improvement - proficiency_penalty)
        
        return round(improvement, 4)
    
    def _calculate_confidence(self, 
                            learning_type: LearningType,
                            data: Dict[str, Any]) -> float:
        """حساب ثقة التعلم"""
        confidence = 0.7  # أساسي
        
        # تعديل حسب نوع التعلم
        type_confidence = {
            LearningType.EXPERIENTIAL: 0.8,
            LearningType.PATTERN: 0.7,
            LearningType.CONCEPTUAL: 0.6,
            LearningType.ADAPTIVE: 0.5
        }
        
        confidence *= type_confidence.get(learning_type, 0.7)
        
        # تعديل حسب جودة البيانات
        data_quality = data.get("quality", 0.5)
        confidence *= (0.5 + data_quality * 0.5)
        
        # تعديل حسب التكرار
        repetition = data.get("repetition", 1)
        if repetition > 3:
            confidence = min(1.0, confidence * 1.2)
        
        return round(confidence, 3)
    
    def _apply_learning_effects(self, 
                               skill: str, 
                               improvement: float,
                               learning_type: LearningType):
        """تطبيق تأثيرات التعلم"""
        effects = []
        
        # تحسين المهارات المرتبطة
        related_skills = self._get_related_skills(skill)
        for related_skill in related_skills:
            if related_skill in self.skill_proficiencies:
                transfer = improvement * 0.3  # نقل التعلم
                self.skill_proficiencies[related_skill] = min(
                    1.0, 
                    self.skill_proficiencies[related_skill] + transfer
                )
                effects.append(f"تحسن {related_skill} بمقدار {round(transfer, 3)}")
        
        # تسجيل التأثيرات
        if effects:
            self.learning_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "learning_transfer",
                "primary_skill": skill,
                "transfer_effects": effects,
                "learning_type": learning_type.value
            })
    
    def _get_related_skills(self, skill: str) -> List[str]:
        """الحصول على المهارات المرتبطة"""
        skill_relations = {
            "dialogue_response": ["context_understanding", "emotion_recognition"],
            "emotion_recognition": ["context_understanding", "pattern_detection"],
            "context_understanding": ["memory_retrieval", "pattern_detection"],
            "pattern_detection": ["memory_retrieval", "context_understanding"],
            "memory_retrieval": ["context_understanding", "pattern_detection"]
        }
        
        return skill_relations.get(skill, [])
    
    def assess_skill_gap(self) -> Dict[str, Any]:
        """تقييم فجوات المهارات"""
        skill_gaps = {}
        
        for skill, proficiency in self.skill_proficiencies.items():
            if proficiency < 0.7:  # مستوى الإتقان المطلوب
                gap = 0.7 - proficiency
                skill_gaps[skill] = {
                    "current_proficiency": round(proficiency, 3),
                    "required_proficiency": 0.7,
                    "gap": round(gap, 3),
                    "priority": "high" if gap > 0.3 else "medium" if gap > 0.1 else "low"
                }
        
        return {
            "total_skills": len(self.skill_proficiencies),
            "skills_below_threshold": len(skill_gaps),
            "average_proficiency": round(
                sum(self.skill_proficiencies.values()) / len(self.skill_proficiencies), 
                3
            ),
            "skill_gaps": skill_gaps,
            "recommended_focus": self._get_recommended_focus(skill_gaps)
        }
    
    def _get_recommended_focus(self, skill_gaps: Dict) -> List[str]:
        """الحصول على مهارات موصى بالتركيز عليها"""
        if not skill_gaps:
            return ["تحسين المهارات المتقدمة"]
        
        # فرز حسب الأولوية والفجوة
        sorted_gaps = sorted(
            skill_gaps.items(),
            key=lambda x: (x[1]["priority"], x[1]["gap"]),
            reverse=True
        )
        
        return [skill for skill, _ in sorted_gaps[:3]]
    
    def get_learning_report(self, days: int = 7) -> Dict[str, Any]:
        """تقرير التعلم لفترة محددة"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_learning = [
            record for record in self.learning_records.values()
            if record.timestamp >= cutoff_date
        ]
        
        if not recent_learning:
            return {
                "period_days": days,
                "total_learning_events": 0,
                "message": "لا أحداث تعلم حديثة"
            }
        
        # تحليل التعلم الحديث
        total_improvement = sum(r.improvement for r in recent_learning)
        avg_efficiency = sum(r.improvement / max(r.duration_minutes, 1) for r in recent_learning) / len(recent_learning)
        
        # توزيع أنواع التعلم
        type_distribution = {}
        for record in recent_learning:
            learning_type = record.learning_type.value
            type_distribution[learning_type] = type_distribution.get(learning_type, 0) + 1
        
        # المهارات الأكثر تحسناً
        skill_improvements = {}
        for record in recent_learning:
            skill = record.skill
            skill_improvements[skill] = skill_improvements.get(skill, 0) + record.improvement
        
        top_skills = sorted(
            skill_improvements.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "period_days": days,
            "total_learning_events": len(recent_learning),
            "total_improvement": round(total_improvement, 3),
            "average_efficiency": round(avg_efficiency, 4),
            "type_distribution": type_distribution,
            "top_improved_skills": [{"skill": s, "improvement": round(i, 3)} for s, i in top_skills],
            "current_proficiencies": {k: round(v, 3) for k, v in self.skill_proficiencies.items()},
            "skill_gap_analysis": self.assess_skill_gap(),
            "report_timestamp": datetime.now().isoformat()
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المعالج"""
        return {
            "total_learning_records": len(self.learning_records),
            "skills_tracked": len(self.skill_proficiencies),
            "learning_history_count": len(self.learning_history),
            "average_proficiency": round(
                sum(self.skill_proficiencies.values()) / len(self.skill_proficiencies), 
                3
            ),
            "last_learning_event": self.learning_history[-1]["timestamp"] if self.learning_history else None
        }


# إنشاء مثيل عالمي لمعالج التعلم
learning_processor = LearningProcessor()
