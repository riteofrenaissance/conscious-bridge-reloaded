"""
Evolution System Package - نظام التطور والتكيف
"""

from .evolution_engine import EvolutionEngine, EvolutionStage, evolution_engine
from .learning_processor import LearningProcessor, LearningRecord, learning_processor
from .adaptation_manager import AdaptationManager, AdaptationStrategy, adaptation_manager
from .maturity_tracker import MaturityTracker, MaturityLevel, maturity_tracker

__all__ = [
    # Evolution Engine
    'EvolutionEngine',
    'EvolutionStage',
    'evolution_engine',
    
    # Learning Processor
    'LearningProcessor',
    'LearningRecord',
    'learning_processor',
    
    # Adaptation Manager
    'AdaptationManager',
    'AdaptationStrategy',
    'adaptation_manager',
    
    # Maturity Tracker
    'MaturityTracker',
    'MaturityLevel',
    'maturity_tracker'
]

__version__ = '2.1.0'
