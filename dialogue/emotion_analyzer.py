"""
Emotion Analyzer - محلل العواطف
يحلل العواطف في النص ويقدم توصيات للاستجابة
"""

from typing import Dict, List, Tuple, Any
import re


class EmotionAnalyzer:
    """المحلل الرئيسي للعواطف"""
    
    def __init__(self):
        # قاموس العواطف العربية
        self.emotion_lexicon = {
            "سعادة": ["سعيد", "فرح", "مسرور", "مبسوط", "بهجة", "ابتهاج", "مرح"],
            "حزن": ["حزين", "تعيس", "مكتئب", "بائس", "كئيب", "مهموم"],
            "غضب": ["غاضب", "غيظ", "مستاء", "منزعج", "مغتاظ", "ثائر"],
            "خوف": ["خائف", "قلق", "مرتعب", "مذعور", "رهبة", "وجل"],
            "دهشة": ["مندهش", "متفاجئ", "صدمة", "مذهول", "متحير"],
            "اشمئزاز": ["مشمئز", "مقرف", "مقزز", "مكروه", "منفر"],
            "توقع": ["متحمس", "متشوق", "منتظر", "مترقب", "شغوف"],
            "حيادية": ["عادي", "طبيعي", "معتدل", "هادئ", "مستقر"]
        }
        
        # أنماط النص الدالة على العواطف
        self.patterns = {
            "سعادة": [r"!+", r":\)", r":D", r"😂", r"😊"],
            "حزن": [r":\(", r"🥲", r"😔", r"😢"],
            "غضب": [r"!{3,}", r"[A-Z][A-Z]+", r"😠", r"👿"],
            "دهشة": [r"\?", r"!?", r"😲", r"🤯"]
        }
        
        self.emotion_intensity = {
            "منخفض": 0.3,
            "متوسط": 0.6,
            "عالي": 0.9
        }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """تحليل النص واستخراج العواطف"""
        if not text or len(text.strip()) == 0:
            return {"primary_emotion": "neutral", "confidence": 0.0, "intensity": 0.0}
        
        text_lower = text.lower()
        
        # اكتشاف العواطف من المفردات
        detected_emotions = self._detect_from_vocabulary(text_lower)
        
        # اكتشاف من الأنماط
        pattern_emotions = self._detect_from_patterns(text)
        
        # دمج النتائج
        all_emotions = self._merge_emotions(detected_emotions, pattern_emotions)
        
        # تحديد العاطفة الأساسية
        primary_emotion, confidence = self._determine_primary_emotion(all_emotions)
        
        # حساب الشدة
        intensity = self._calculate_intensity(text, primary_emotion)
        
        # توليد توصيات للاستجابة
        response_recommendations = self._generate_recommendations(primary_emotion, intensity)
        
        return {
            "primary_emotion": primary_emotion,
            "confidence": round(confidence, 3),
            "intensity": round(intensity, 3),
            "all_emotions": all_emotions,
            "text_length": len(text),
            "word_count": len(text.split()),
            "response_recommendations": response_recommendations,
            "analysis_method": "lexicon_and_pattern"
        }
    
    def _detect_from_vocabulary(self, text: str) -> Dict[str, float]:
        """اكتشاف العواطف من المفردات"""
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_lexicon.items():
            score = 0.0
            for keyword in keywords:
                if keyword in text:
                    # زيادة النقاط لكل تكرار
                    occurrences = text.count(keyword)
                    score += min(0.5, occurrences * 0.1)
            
            if score > 0:
                emotion_scores[emotion] = min(1.0, score)
        
        return emotion_scores
    
    def _detect_from_patterns(self, text: str) -> Dict[str, float]:
        """اكتشاف العواطف من الأنماط"""
        emotion_scores = {}
        
        for emotion, patterns in self.patterns.items():
            score = 0.0
            for pattern in patterns:
                matches = re.findall(pattern, text)
                if matches:
                    score += min(0.3, len(matches) * 0.1)
            
            if score > 0:
                emotion_scores[emotion] = min(1.0, score)
        
        return emotion_scores
    
    def _merge_emotions(self, vocab_emotions: Dict, pattern_emotions: Dict) -> Dict[str, float]:
        """دمج نتائج اكتشاف العواطف"""
        merged = {}
        
        # جميع العواطف الممكنة
        all_emotions = set(list(vocab_emotions.keys()) + list(pattern_emotions.keys()))
        
        for emotion in all_emotions:
            vocab_score = vocab_emotions.get(emotion, 0.0)
            pattern_score = pattern_emotions.get(emotion, 0.0)
            
            # الوزن: 70% للمفردات، 30% للأنماط
            merged_score = (vocab_score * 0.7) + (pattern_score * 0.3)
            if merged_score > 0:
                merged[emotion] = round(merged_score, 3)
        
        # إذا لم تكتشف أي عاطفة
        if not merged:
            merged["حيادية"] = 0.5
        
        return merged
    
    def _determine_primary_emotion(self, emotions: Dict[str, float]) -> Tuple[str, float]:
        """تحديد العاطفة الأساسية"""
        if not emotions:
            return "حيادية", 0.0
        
        primary_emotion = max(emotions.items(), key=lambda x: x[1])
        return primary_emotion[0], primary_emotion[1]
    
    def _calculate_intensity(self, text: str, primary_emotion: str) -> float:
        """حساب شدة العاطفة"""
        intensity = 0.5  # أساسي
        
        # عوامل زيادة الشدة
        if len(text) > 100:
            intensity += 0.1
        
        if "!" in text:
            exclamation_count = text.count("!")
            intensity += min(0.3, exclamation_count * 0.05)
        
        if text.isupper():
            intensity += 0.2
        
        # بعض العواطف تكون أكثر شدة بطبيعتها
        intense_emotions = ["غضب", "خوف", "دهشة"]
        if primary_emotion in intense_emotions:
            intensity += 0.1
        
        return min(1.0, intensity)
    
    def _generate_recommendations(self, emotion: str, intensity: float) -> List[str]:
        """توليد توصيات للاستجابة"""
        recommendations = []
        
        if emotion == "سعادة":
            recommendations.append("الحفاظ على النبرة الإيجابية")
            if intensity > 0.7:
                recommendations.append("المشاركة في الفرح")
            recommendations.append("تشجيع الاستمرارية")
        
        elif emotion == "حزن":
            recommendations.append("استخدام نبرة تعاطفية")
            recommendations.append("تقديم الدعم المعنوي")
            if intensity > 0.7:
                recommendations.append("تجنب المزاح أو التفاؤل المفرط")
        
        elif emotion == "غضب":
            recommendations.append("استخدام نبرة هادئة")
            recommendations.append("الاعتراف بالمشاعر")
            recommendations.append("تجنب التحدي أو الجدال")
        
        elif emotion == "خوف":
            recommendations.append("تقديم الطمأنينة")
            recommendations.append("توضيح المعلومات")
            recommendations.append("استخدام لغة واضحة ومباشرة")
        
        else:  # حيادية أو أخرى
            recommendations.append("الرد بشكل واضح ومباشر")
            recommendations.append("تقديم المعلومات بدقة")
        
        # إضافة توصيات عامة
        recommendations.append("التحقق من فهم المستخدم")
        recommendations.append("توفير خيارات للمتابعة")
        
        return recommendations
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المحلل"""
        return {
            "emotions_tracked": len(self.emotion_lexicon),
            "total_keywords": sum(len(keywords) for keywords in self.emotion_lexicon.values()),
            "patterns_count": len(self.patterns),
            "intensity_levels": list(self.emotion_intensity.keys())
        }


# إنشاء مثيل عالمي لمحلل العواطف
emotion_analyzer = EmotionAnalyzer()
