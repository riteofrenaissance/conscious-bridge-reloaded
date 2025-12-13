"""
Dialogue Analyzer - محلل الحوارات
يحلل جلسات الحوار ويستخرج إحصائيات وأنماط
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from .dialogue_manager import dialogue_manager


class DialogueAnalyzer:
    """المحلل الرئيسي للحوارات"""
    
    def __init__(self):
        self.analysis_history = []
        self.patterns_detected = []
        
    def analyze_session(self, session_id: str) -> Dict[str, Any]:
        """تحليل جلسة حوار محددة"""
        session = dialogue_manager.get_session(session_id)
        
        if not session or not session.turns:
            return {"error": "Session not found or empty"}
        
        turns = session.turns
        user_turns = [t for t in turns if t.speaker == "user"]
        ai_turns = [t for t in turns if t.speaker == "ai"]
        
        # تحليل أساسي
        analysis = {
            "session_id": session_id,
            "user_id": session.user_id,
            "total_turns": len(turns),
            "user_turns": len(user_turns),
            "ai_turns": len(ai_turns),
            "turn_ratio": round(len(ai_turns) / max(len(user_turns), 1), 2),
            "duration_seconds": None,
            "average_turn_length": self._calculate_avg_turn_length(turns),
            "emotion_distribution": self._analyze_emotions(turns),
            "topics_detected": self._detect_topics(turns),
            "interaction_pattern": self._identify_pattern(turns),
            "quality_score": self._calculate_quality_score(turns),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # حساب المدة إذا كانت الجلسة منتهية
        if session.end_time:
            duration = (session.end_time - session.start_time).total_seconds()
            analysis["duration_seconds"] = round(duration, 2)
            analysis["turns_per_minute"] = round(len(turns) / (duration / 60), 2)
        
        # حفظ التحليل
        self.analysis_history.append({
            "session_id": session_id,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
        
        # اكتشاف الأنماط
        detected_patterns = self._detect_patterns(analysis)
        if detected_patterns:
            self.patterns_detected.extend(detected_patterns)
            analysis["patterns_detected"] = detected_patterns
        
        return analysis
    
    def _calculate_avg_turn_length(self, turns: List) -> Dict[str, float]:
        """حساب متوسط طول الأدوار"""
        if not turns:
            return {"user": 0.0, "ai": 0.0, "overall": 0.0}
        
        user_lengths = [len(t.content.split()) for t in turns if t.speaker == "user"]
        ai_lengths = [len(t.content.split()) for t in turns if t.speaker == "ai"]
        
        return {
            "user": round(sum(user_lengths) / len(user_lengths), 2) if user_lengths else 0.0,
            "ai": round(sum(ai_lengths) / len(ai_lengths), 2) if ai_lengths else 0.0,
            "overall": round(sum(len(t.content.split()) for t in turns) / len(turns), 2)
        }
    
    def _analyze_emotions(self, turns: List) -> Dict[str, int]:
        """تحليل توزيع العواطف"""
        emotion_counter = Counter()
        
        for turn in turns:
            emotion = getattr(turn, 'emotion', 'neutral')
            emotion_counter[emotion] += 1
        
        return dict(emotion_counter)
    
    def _detect_topics(self, turns: List) -> List[str]:
        """اكتشاف المواضيع الرئيسية"""
        common_topics = {
            "greeting": ["مرحباً", "أهلاً", "سلام", "السلام"],
            "question": ["ما هو", "كيف", "لماذا", "أين", "متى", "من"],
            "technical": ["برمجة", "كود", "نظام", "ذاكرة", "حوار", "تطوير"],
            "help": ["مساعدة", "مساعد", "ساعد", "دعم", "شرح"],
            "feedback": ["شكراً", "متشكر", "جيد", "سيء", "ممتاز", "تحسين"]
        }
        
        detected = set()
        all_text = " ".join([t.content.lower() for t in turns])
        
        for topic, keywords in common_topics.items():
            if any(keyword in all_text for keyword in keywords):
                detected.add(topic)
        
        return list(detected)
    
    def _identify_pattern(self, turns: List) -> str:
        """تحديد نمط التفاعل"""
        if len(turns) < 3:
            return "short"
        
        user_turns = [t for t in turns if t.speaker == "user"]
        ai_turns = [t for t in turns if t.speaker == "ai"]
        
        # تحليل أطوال الأدوار
        avg_user_len = sum(len(t.content.split()) for t in user_turns) / len(user_turns)
        avg_ai_len = sum(len(t.content.split()) for t in ai_turns) / len(ai_turns)
        
        if avg_user_len > 20 and avg_ai_len > 30:
            return "deep_discussion"
        elif avg_user_len < 5 and avg_ai_len < 10:
            return "brief_exchange"
        elif len(turns) > 10:
            return "extended_conversation"
        else:
            return "standard_interaction"
    
    def _calculate_quality_score(self, turns: List) -> float:
        """حساب درجة جودة الحوار"""
        if len(turns) < 2:
            return 0.5
        
        score = 0.5  # أساسي
        
        # عوامل إيجابية
        if len(turns) >= 5:
            score += 0.2
        
        # تنوع العواطف
        emotions = self._analyze_emotions(turns)
        if len(emotions) > 1:
            score += 0.1
        
        # تناوب الأدوار الجيد
        if all(turns[i].speaker != turns[i+1].speaker for i in range(len(turns)-1)):
            score += 0.1
        
        # طول مناسب
        avg_len = self._calculate_avg_turn_length(turns)["overall"]
        if 5 <= avg_len <= 30:
            score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _detect_patterns(self, analysis: Dict) -> List[str]:
        """اكتشاف أنماط في التحليل"""
        patterns = []
        
        # نمط: حوار عميق
        if analysis.get("interaction_pattern") == "deep_discussion":
            patterns.append("deep_learning_dialogue")
        
        # نمط: أسئلة متكررة
        if analysis.get("total_turns", 0) > 8 and "question" in analysis.get("topics_detected", []):
            patterns.append("inquisitive_session")
        
        # نمط: عواطف قوية
        emotions = analysis.get("emotion_distribution", {})
        if any(emotion in emotions for emotion in ["happy", "angry", "excited"]) and sum(emotions.values()) > 2:
            patterns.append("emotional_engagement")
        
        return patterns
    
    def analyze_recent_sessions(self, hours: int = 24, limit: int = 10) -> Dict[str, Any]:
        """تحليل الجلسات الحديثة"""
        recent_time = datetime.now() - timedelta(hours=hours)
        
        all_sessions = []
        for session in dialogue_manager.sessions.values():
            if session.start_time >= recent_time:
                all_sessions.append(session)
        
        all_sessions.sort(key=lambda s: s.start_time, reverse=True)
        recent_sessions = all_sessions[:limit]
        
        if not recent_sessions:
            return {"recent_sessions_count": 0}
        
        # تحليل إحصائي
        total_turns = sum(len(s.turns) for s in recent_sessions)
        active_sessions = sum(1 for s in recent_sessions if s.is_active)
        
        # جمع المواضيع
        all_topics = set()
        for session in recent_sessions:
            analysis = self.analyze_session(session.session_id)
            topics = analysis.get("topics_detected", [])
            all_topics.update(topics)
        
        return {
            "recent_sessions_count": len(recent_sessions),
            "active_sessions": active_sessions,
            "total_recent_turns": total_turns,
            "average_turns_per_session": round(total_turns / len(recent_sessions), 2),
            "common_topics": list(all_topics),
            "time_period_hours": hours,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المحلل"""
        return {
            "total_analyses": len(self.analysis_history),
            "patterns_detected_count": len(self.patterns_detected),
            "unique_patterns": len(set(self.patterns_detected)),
            "last_analysis": self.analysis_history[-1]["timestamp"] if self.analysis_history else None
        }


# إنشاء مثيل عالمي لمحلل الحوارات
dialogue_analyzer = DialogueAnalyzer()
