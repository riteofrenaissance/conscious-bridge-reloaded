"""
Response Generator - مولد الردود الذكية
يولد ردوداً ذكية بناءً على السياق والذاكرة
"""

from typing import Dict, List, Optional, Any
import random
from datetime import datetime
from ..memory.memory_manager import memory_manager


class ResponseGenerator:
    """المولد الرئيسي للردود"""
    
    def __init__(self):
        self.response_templates = {
            "greeting": [
                "مرحباً! كيف يمكنني مساعدتك اليوم؟",
                "أهلاً بك! أنا هنا لمساعدتك.",
                "مرحباً بك! كيف حالك؟"
            ],
            "question": [
                "هذا سؤال ممتاز. دعني أفكر في الأمر...",
                "أفهم سؤالك. إليك ما أعرفه:",
                "شكراً لسؤالك. هذا ما لدي من معلومات:"
            ],
            "thanks": [
                "العفو! سعيد لأنني استطعت المساعدة.",
                "لا شكر على واجب! دائماً هنا لمساعدتك.",
                "شكراً لك! أي شيء آخر تحتاج إليه؟"
            ],
            "unknown": [
                "أحتاج إلى مزيد من التفاصيل لفهم سؤالك.",
                "هل يمكنك إعادة صياغة سؤالك بطريقة أخرى؟",
                "أعتذر، لم أفهم ذلك تماماً. هل يمكنك التوضيح؟"
            ],
            "learning": [
                "شكراً لك على تعليمي هذا! سأتذكر هذه المعلومة.",
                "ممتاز! لقد تعلمت شيئاً جديداً اليوم.",
                "هذه معلومة قيمة. شكراً للمشاركة!"
            ]
        }
        
        self.knowledge_base = {
            "conscious_bridge": [
                "Conscious Bridge هو نظام ذكاء اصطناعي تفاعلي",
                "النظام يتطور باستمرار من خلال التفاعل مع المستخدمين",
                "يتمتع النظام بذاكرة عميقة تسمح له بالتعلم من التجارب"
            ],
            "memory": [
                "نظام الذاكرة يحفظ التفاعلات والخبرات",
                "يمكن للنظام استخلاص أفكار من التجارب السابقة",
                "الذاكرة تدمج المعلومات المتشابهة في مفاهيم أعلى"
            ],
            "dialogue": [
                "نظام الحوار يتفاعل بشكل طبيعي مع المستخدمين",
                "يمكن للنظام تحليل العواطف والاستجابة بشكل مناسب",
                "الحوار يسجل ويحلل للتحسين المستمر"
            ]
        }
    
    def generate_response(self, 
                         user_input: str, 
                         session_id: str,
                         context: Dict[str, Any] = None) -> Dict[str, Any]:
        """توليد رد ذكي بناءً على المدخلات"""
        if context is None:
            context = {}
        
        # تحليل نوع المدخلات
        input_type = self._classify_input(user_input)
        
        # البحث في الذاكرة عن معلومات ذات صلة
        memory_context = self._get_memory_context(user_input)
        
        # توليد الرد
        response_text = self._generate_response_text(user_input, input_type, memory_context)
        
        # تحليل العاطفة المطلوبة للرد
        emotion = self._determine_emotion(user_input, response_text)
        
        # حساب الثقة في الرد
        confidence = self._calculate_confidence(user_input, input_type, memory_context)
        
        # حفظ التفاعل في الذاكرة
        memory_result = memory_manager.process_interaction(user_input, response_text)
        
        return {
            "response": response_text,
            "emotion": emotion,
            "confidence": round(confidence, 2),
            "input_type": input_type,
            "memory_context": memory_context,
            "memory_recorded": memory_result,
            "timestamp": datetime.now().isoformat()
        }
    
    def _classify_input(self, text: str) -> str:
        """تصنيف المدخلات"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["مرحباً", "أهلاً", "سلام", "السلام عليكم"]):
            return "greeting"
        elif any(word in text_lower for word in ["شكراً", "متشكر", "ممتن", "يعطيك العافية"]):
            return "thanks"
        elif "؟" in text or "?" in text or any(word in text_lower for word in ["ما هو", "كيف", "لماذا", "أين"]):
            return "question"
        elif any(word in text_lower for word in ["تعلم", "تعرف", "اعرف", "معلومات"]):
            return "learning"
        else:
            return "general"
    
    def _get_memory_context(self, query: str) -> List[str]:
        """الحصول على سياق من الذاكرة"""
        # هذا سيكون بحثاً حقيقياً في الذاكرة في الإصدار الكامل
        context = []
        
        # بحث بسيط في قاعدة المعرفة
        for topic, facts in self.knowledge_base.items():
            if any(word in query.lower() for word in topic.split("_")):
                context.extend(facts[:2])  # أول حقيقتين فقط
        
        return context[:3]  # إرجاع أول 3 عناصر فقط
    
    def _generate_response_text(self, 
                               user_input: str, 
                               input_type: str,
                               memory_context: List[str]) -> str:
        """توليد نص الرد"""
        # البدء بقالب مناسب
        templates = self.response_templates.get(input_type, self.response_templates["unknown"])
        base_response = random.choice(templates)
        
        # إضافة معلومات من الذاكرة إذا كانت متوفرة
        if memory_context:
            memory_info = " ".join(memory_context[:2])
            response = f"{base_response} {memory_info}"
        else:
            response = base_response
        
        # تخصيص الرد بناءً على المدخلات
        if "اسمك" in user_input or "من أنت" in user_input:
            response = "أنا Conscious Bridge، نظام ذكاء اصطناعي تفاعلي. أسعد بتقديم المساعدة!"
        elif "ذاكرة" in user_input:
            response = "نظام الذاكرة الخاص بي يسمح لي بتذكر تفاعلاتنا وتعلم منها باستمرار."
        
        return response
    
    def _determine_emotion(self, user_input: str, response: str) -> str:
        """تحديد العاطفة المناسبة للرد"""
        positive_words = ["شكراً", "ممتاز", "رائع", "جميل", "جيد", "مدهش"]
        negative_words = ["مشكلة", "خطأ", "سيء", "لا", "لماذا", "كيف"]
        
        user_input_lower = user_input.lower()
        response_lower = response.lower()
        
        if any(word in user_input_lower for word in positive_words):
            return "positive"
        elif any(word in user_input_lower for word in negative_words):
            return "neutral"  # الحيادية مع المدخلات السلبية
        elif "؟" in user_input or "?" in user_input:
            return "curious"
        else:
            return "neutral"
    
    def _calculate_confidence(self, 
                            user_input: str, 
                            input_type: str,
                            memory_context: List[str]) -> float:
        """حساب ثقة النظام في الرد"""
        confidence = 0.5  # أساسي
        
        # زيادة الثقة بناءً على السياق
        if memory_context:
            confidence += 0.3
        
        # زيادة الثقة لأنواع المدخلات المعروفة
        if input_type in ["greeting", "thanks"]:
            confidence += 0.2
        
        # تقليل الثقة للمدخلات الطويلة المعقدة
        if len(user_input.split()) > 20:
            confidence -= 0.1
        
        return max(0.1, min(1.0, confidence))
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المولد"""
        return {
            "templates_count": {k: len(v) for k, v in self.response_templates.items()},
            "knowledge_topics": list(self.knowledge_base.keys()),
            "total_knowledge_facts": sum(len(facts) for facts in self.knowledge_base.values())
        }


# إنشاء مثيل عالمي لمولد الردود
response_generator = ResponseGenerator()
