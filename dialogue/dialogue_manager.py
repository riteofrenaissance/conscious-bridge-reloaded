"""
Dialogue Manager - مدير الحوار التفاعلي
يدير محادثات الذكاء الاصطناعي مع المستخدمين
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid


class DialogueTurn:
    """دورة حوار واحدة"""
    
    def __init__(self, speaker: str, content: str, 
                 emotion: str = "neutral", confidence: float = 1.0):
        self.id = str(uuid.uuid4())[:8]
        self.speaker = speaker  # "user" أو "ai"
        self.content = content
        self.emotion = emotion
        self.confidence = confidence
        self.timestamp = datetime.now()
        self.metadata = {}
    
    def to_dict(self) -> Dict:
        """تحويل إلى قاموس"""
        return {
            "id": self.id,
            "speaker": self.speaker,
            "content": self.content,
            "emotion": self.emotion,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


class DialogueSession:
    """جلسة حوار كاملة"""
    
    def __init__(self, session_id: str = None, user_id: str = "anonymous"):
        self.session_id = session_id or str(uuid.uuid4())[:12]
        self.user_id = user_id
        self.turns: List[DialogueTurn] = []
        self.start_time = datetime.now()
        self.end_time = None
        self.context = {}
        self.is_active = True
    
    def add_turn(self, speaker: str, content: str, **kwargs) -> DialogueTurn:
        """إضافة دورة حوار جديدة"""
        turn = DialogueTurn(speaker, content, **kwargs)
        self.turns.append(turn)
        return turn
    
    def get_last_turn(self) -> Optional[DialogueTurn]:
        """الحصول على آخر دورة حوار"""
        return self.turns[-1] if self.turns else None
    
    def get_turns_by_speaker(self, speaker: str) -> List[DialogueTurn]:
        """الحصول على أدوار متحدث معين"""
        return [turn for turn in self.turns if turn.speaker == speaker]
    
    def end_session(self):
        """إنهاء الجلسة"""
        self.end_time = datetime.now()
        self.is_active = False
    
    def to_dict(self) -> Dict:
        """تحويل الجلسة إلى قاموس"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "turns": [turn.to_dict() for turn in self.turns],
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "turn_count": len(self.turns),
            "is_active": self.is_active
        }


class DialogueManager:
    """المدير الرئيسي للحوارات"""
    
    def __init__(self):
        self.sessions: Dict[str, DialogueSession] = {}
        self.active_sessions = 0
    
    def create_session(self, user_id: str = "anonymous") -> DialogueSession:
        """إنشاء جلسة حوار جديدة"""
        session = DialogueSession(user_id=user_id)
        self.sessions[session.session_id] = session
        self.active_sessions += 1
        return session
    
    def get_session(self, session_id: str) -> Optional[DialogueSession]:
        """الحصول على جلسة بواسطة المعرف"""
        return self.sessions.get(session_id)
    
    def end_session(self, session_id: str):
        """إنهاء جلسة محددة"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.end_session()
            if session.is_active:
                self.active_sessions -= 1
    
    def get_statistics(self) -> Dict:
        """الحصول على إحصائيات المدير"""
        total_turns = sum(len(session.turns) for session in self.sessions.values())
        avg_turns = total_turns / len(self.sessions) if self.sessions else 0
        
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": self.active_sessions,
            "total_turns": total_turns,
            "average_turns_per_session": round(avg_turns, 1)
        }


# إنشاء مثيل عالمي لمدير الحوار
dialogue_manager = DialogueManager()

