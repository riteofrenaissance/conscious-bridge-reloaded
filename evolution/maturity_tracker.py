"""
Maturity Tracker - متتبع النضج
يتتبع نضج النظام عبر الأبعاد المختلفة
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


class MaturityDimension(Enum):
    """أبعاد النضج"""
    COGNITIVE = "cognitive"      # معرفي
    SOCIAL = "social"            # اجتماعي
    EMOTIONAL = "emotional"      # عاطفي
    ADAPTIVE = "adaptive"        # تكيفي
    AUTONOMOUS = "autonomous"    # ذاتي


@dataclass
class MaturityLevel:
    """مستوى النضج"""
    dimension: MaturityDimension
    score: float  # 0.0-1.0
    confidence: float
    last_assessment: datetime
    trend: str  # improving, stable, declining
    indicators: List[str]
    
    def to_dict(self) -> Dict:
        """تحويل إلى قاموس"""
        return {
            "dimension": self.dimension.value,
            "score": round(self.score, 3),
            "confidence": round(self.confidence, 3),
            "last_assessment": self.last_assessment.isoformat(),
            "trend": self.trend,
            "indicators": self.indicators,
            "label": self._get_label()
        }
    
    def _get_label(self) -> str:
        """الحصول على تسمية المستوى"""
        if self.score < 0.3:
            return "ابتدائي"
        elif self.score < 0.5:
            return "متطور"
        elif self.score < 0.7:
            return "متقدم"
        elif self.score < 0.9:
            return "ناضج"
        else:
            return "متميز"


class MaturityTracker:
    """المتتبع الرئيسي للنضج"""
    
    def __init__(self):
        self.maturity_levels: Dict[MaturityDimension, MaturityLevel] = {}
        self.assessment_history: List[Dict] = []
        self.last_full_assessment = None
        self._initialize_levels()
    
    def _initialize_levels(self):
        """تهيئة مستويات النضج الأولية"""
        initial_data = [
            (MaturityDimension.COGNITIVE, 0.3, ["معرفة أساسية", "فهم محدود"]),
            (MaturityDimension.SOCIAL, 0.2, ["تفاعل أساسي", "استجابات نمطية"]),
            (MaturityDimension.EMOTIONAL, 0.1, ["تمييز عواطف أساسية"]),
            (MaturityDimension.ADAPTIVE, 0.2, ["تكيف بسيط"]),
            (MaturityDimension.AUTONOMOUS, 0.1, ["اعتماد على التوجيه"])
        ]
        
        for dimension, score, indicators in initial_data:
            self.maturity_levels[dimension] = MaturityLevel(
                dimension=dimension,
                score=score,
                confidence=0.5,
                last_assessment=datetime.now(),
                trend="stable",
                indicators=indicators
            )
    
    def assess_maturity(self) -> Dict[str, Any]:
        """تقييم النضج الشامل"""
        assessments = {}
        total_score = 0
        
        for dimension in MaturityDimension:
            assessment = self._assess_dimension(dimension)
            assessments[dimension.value] = assessment
            
            if dimension in self.maturity_levels:
                old_score = self.maturity_levels[dimension].score
                self.maturity_levels[dimension] = MaturityLevel(
                    dimension=dimension,
                    score=assessment["score"],
                    confidence=assessment["confidence"],
                    last_assessment=datetime.now(),
                    trend=self._calculate_trend(old_score, assessment["score"]),
                    indicators=assessment["key_indicators"]
                )
            
            total_score += assessment["score"]
        
        overall_maturity = total_score / len(MaturityDimension)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "overall_maturity": round(overall_maturity, 3),
            "overall_label": self._get_overall_label(overall_maturity),
            "dimension_assessments": assessments,
            "trend_analysis": self._analyze_trends(),
            "strengths": self._identify_strengths(assessments),
            "improvement_areas": self._identify_improvement_areas(assessments),
            "recommendations": self._generate_maturity_recommendations(assessments)
        }
        
        self.assessment_history.append(report)
        self.last_full_assessment = datetime.now()
        
        return report
    
    def _assess_dimension(self, dimension: MaturityDimension) -> Dict[str, Any]:
        """تقييم بُعد نضج محدد"""
        # قيم افتراضية للاختبار
        if dimension == MaturityDimension.COGNITIVE:
            return {
                "score": 0.35,
                "confidence": 0.6,
                "key_indicators": ["معرفة متوسطة", "فهم أساسي"],
                "component_scores": {"knowledge": 0.4, "learning": 0.3}
            }
        elif dimension == MaturityDimension.SOCIAL:
            return {
                "score": 0.25,
                "confidence": 0.5,
                "key_indicators": ["تفاعل بسيط", "استجابات محدودة"],
                "component_scores": {"interaction": 0.3, "quality": 0.2}
            }
        elif dimension == MaturityDimension.EMOTIONAL:
            return {
                "score": 0.15,
                "confidence": 0.4,
                "key_indicators": ["تمييز عواطف أساسية"],
                "component_scores": {"emotion_topics": 0.2, "emotion_variety": 0.1}
            }
        elif dimension == MaturityDimension.ADAPTIVE:
            return {
                "score": 0.25,
                "confidence": 0.5,
                "key_indicators": ["تكيف محدود"],
                "component_scores": {"adaptation_frequency": 0.3, "proactivity": 0.2}
            }
        else:  # AUTONOMOUS
            return {
                "score": 0.15,
                "confidence": 0.4,
                "key_indicators": ["اعتماد على التوجيه"],
                "component_scores": {"evolution_stage": 0.2, "experience_autonomy": 0.1}
            }
    
    def _calculate_trend(self, old_score: float, new_score: float) -> str:
        """حساب اتجاه التغيير"""
        diff = new_score - old_score
        
        if diff > 0.05:
            return "improving"
        elif diff < -0.05:
            return "declining"
        else:
            return "stable"
    
    def _get_overall_label(self, score: float) -> str:
        """الحصول على تسمية النضج العام"""
        if score < 0.2:
            return "وليد"
        elif score < 0.4:
            return "ناشئ"
        elif score < 0.6:
            return "متطور"
        elif score < 0.8:
            return "ناضج"
        else:
            return "متميز"
    
    def _analyze_trends(self) -> Dict[str, Any]:
        """تحليل اتجاهات النضج"""
        if len(self.assessment_history) < 2:
            return {"status": "insufficient_data", "message": "بحاجة لمزيد من التقييمات"}
        
        return {
            "period_assessments": len(self.assessment_history),
            "overall_trend": "improving"
        }
    
    def _identify_strengths(self, assessments: Dict) -> List[Dict]:
        """تحديد نقاط القوة"""
        strengths = []
        
        for dim_name, assessment in assessments.items():
            if assessment["score"] >= 0.3:
                strengths.append({
                    "dimension": dim_name,
                    "score": assessment["score"],
                    "indicators": assessment["key_indicators"][:1]
                })
        
        return strengths[:2]
    
    def _identify_improvement_areas(self, assessments: Dict) -> List[Dict]:
        """تحديد مجالات التحسين"""
        improvements = []
        
        for dim_name, assessment in assessments.items():
            if assessment["score"] < 0.3:
                improvements.append({
                    "dimension": dim_name,
                    "score": assessment["score"],
                    "priority": "high",
                    "suggestions": [f"تحسين {dim_name} من خلال المزيد من التفاعل"]
                })
        
        return improvements
    
    def _generate_maturity_recommendations(self, assessments: Dict) -> List[str]:
        """توليد توصيات للنضج"""
        recommendations = [
            "زيادة التفاعل مع النظام",
            "تنويع أنواع الأسئلة والمواضيع",
            "تشجيع الحوارات المتعمقة"
        ]
        
        return recommendations
    
    def get_current_maturity_levels(self) -> Dict[str, Any]:
        """الحصول على مستويات النضج الحالية"""
        levels_dict = {}
        for dimension, level in self.maturity_levels.items():
            levels_dict[dimension.value] = level.to_dict()
        
        if levels_dict:
            overall_score = sum(level["score"] for level in levels_dict.values()) / len(levels_dict)
        else:
            overall_score = 0.0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_maturity": round(overall_score, 3),
            "overall_label": self._get_overall_label(overall_score),
            "dimensions": levels_dict,
            "last_full_assessment": self.last_full_assessment.isoformat() if self.last_full_assessment else None,
            "assessment_count": len(self.assessment_history)
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المتتبع"""
        return {
            "dimensions_tracked": len(self.maturity_levels),
            "assessment_history_count": len(self.assessment_history),
            "last_assessment": self.assessment_history[-1]["timestamp"] if self.assessment_history else None
        }


# إنشاء مثيل عالمي لمتتبع النضج
maturity_tracker = MaturityTracker()
