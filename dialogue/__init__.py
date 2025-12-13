"""
Dialogue System Package - نظام الحوار التفاعلي
"""

from .dialogue_manager import DialogueManager, DialogueSession, DialogueTurn, dialogue_manager
from .response_generator import ResponseGenerator, response_generator
from .emotion_analyzer import EmotionAnalyzer, emotion_analyzer
from .dialogue_analyzer import DialogueAnalyzer, dialogue_analyzer

__all__ = [
    # Dialogue Manager
    'DialogueManager',
    'DialogueSession', 
    'DialogueTurn',
    'dialogue_manager',
    
    # Response Generator
    'ResponseGenerator',
    'response_generator',
    
    # Emotion Analyzer
    'EmotionAnalyzer',
    'emotion_analyzer',
    
    # Dialogue Analyzer
    'DialogueAnalyzer',
    'dialogue_analyzer'
]

__version__ = '2.1.0'
