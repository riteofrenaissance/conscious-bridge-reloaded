"""
Memory System Package - نظام الذاكرة المتكامل
"""

from .deep_memory import DeepMemory, MemoryEntry, MemoryType, MemoryPriority, memory_system
from .experience_store import ExperienceStore, experience_store
from .insight_tracker import InsightTracker, Insight, insight_tracker
from .consolidation_engine import ConsolidationEngine, MemoryCluster, consolidation_engine

__all__ = [
    # Deep Memory
    'DeepMemory',
    'MemoryEntry', 
    'MemoryType',
    'MemoryPriority',
    'memory_system',
    
    # Experience Store
    'ExperienceStore',
    'experience_store',
    
    # Insight Tracker
    'InsightTracker',
    'Insight', 
    'insight_tracker',
    
    # Consolidation Engine
    'ConsolidationEngine',
    'MemoryCluster',
    'consolidation_engine'
]

__version__ = '2.1.0'
