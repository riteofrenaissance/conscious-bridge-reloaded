"""
Dialogue module for Conscious Bridge Reloaded
Handles communication between bridges
"""

from .dialogue_engine import DialogueEngine, Dialogue, DialogueMessage
from .conversation_analyzer import ConversationAnalyzer
from .semantic_bridge import SemanticBridge, SemanticConnection

__all__ = [
    'DialogueEngine',
    'Dialogue',
    'DialogueMessage',
    'ConversationAnalyzer',
    'SemanticBridge',
    'SemanticConnection'
]
