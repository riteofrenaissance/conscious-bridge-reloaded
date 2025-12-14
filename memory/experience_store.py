"""
Experience Store
Specialized storage for experiences
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class StoredExperience:
    """A stored experience with metadata"""
    id: str
    experience_data: Dict
    tick: int
    processing_quality: float  # 0.0 - 1.0
    insights_generated: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    processed: bool = False


class ExperienceStore:
    """
    Specialized store for experiences
    
    Features:
    - Categorization by type and quality
    - Quick retrieval by criteria
    - Experience chain tracking
    - Quality analysis
    """
    
    def __init__(self):
        self.experiences: Dict[str, StoredExperience] = {}
        self.experience_chains: Dict[str, List[str]] = {}  # chain_id -> experience_ids
        self.quality_stats: Dict[str, List[float]] = {}  # type -> list of qualities
        
    def store_experience(self, experience_data: Dict, tick: int, processing_quality: float, tags: List[str] = None) -> str:
        """Store a new experience"""
        exp_id = f"exp_{len(self.experiences) + 1}"
        
        experience = StoredExperience(
            id=exp_id,
            experience_data=experience_data,
            tick=tick,
            processing_quality=processing_quality,
            tags=tags or []
        )
        
        self.experiences[exp_id] = experience
        
        # Update quality statistics
        exp_type = experience_data.get("type", "unknown")
        if exp_type not in self.quality_stats:
            self.quality_stats[exp_type] = []
        self.quality_stats[exp_type].append(processing_quality)
        
        return exp_id
    
    def get_experience(self, exp_id: str) -> Optional[StoredExperience]:
        """Get an experience by ID"""
        return self.experiences.get(exp_id)
    
    def get_recent_experiences(self, count: int = 10) -> List[StoredExperience]:
        """Get most recent experiences"""
        experiences = list(self.experiences.values())
        experiences.sort(key=lambda x: x.timestamp, reverse=True)
        return experiences[:count]
    
    def get_experiences_by_type(self, exp_type: str) -> List[StoredExperience]:
        """Get experiences by type"""
        return [
            exp for exp in self.experiences.values()
            if exp.experience_data.get("type") == exp_type
        ]
    
    def get_high_quality_experiences(self, threshold: float = 0.7) -> List[StoredExperience]:
        """Get experiences with high processing quality"""
        return [
            exp for exp in self.experiences.values()
            if exp.processing_quality >= threshold
        ]
    
    def mark_processed(self, exp_id: str, insight_ids: List[str] = None):
        """Mark an experience as processed"""
        if exp_id in self.experiences:
            self.experiences[exp_id].processed = True
            if insight_ids:
                self.experiences[exp_id].insights_generated.extend(insight_ids)
    
    def create_experience_chain(self, experience_ids: List[str], chain_type: str = "sequential") -> str:
        """Create a chain of related experiences"""
        chain_id = f"chain_{len(self.experience_chains) + 1}"
        self.experience_chains[chain_id] = experience_ids
        
        # Tag the experiences as part of this chain
        for exp_id in experience_ids:
            if exp_id in self.experiences:
                self.experiences[exp_id].tags.append(f"chain:{chain_id}")
                self.experiences[exp_id].tags.append(f"chain_type:{chain_type}")
        
        return chain_id
    
    def get_quality_stats(self) -> Dict:
        """Get quality statistics by experience type"""
        stats = {}
        
        for exp_type, qualities in self.quality_stats.items():
            if qualities:
                stats[exp_type] = {
                    "count": len(qualities),
                    "average_quality": round(sum(qualities) / len(qualities), 3),
                    "max_quality": round(max(qualities), 3),
                    "min_quality": round(min(qualities), 3)
                }
        
        # Overall statistics
        all_qualities = []
        for qualities in self.quality_stats.values():
            all_qualities.extend(qualities)
        
        if all_qualities:
            stats["overall"] = {
                "total_experiences": len(all_qualities),
                "average_quality": round(sum(all_qualities) / len(all_qualities), 3)
            }
        
        return stats
    
    def get_experience_flow(self, window_size: int = 100) -> List[Dict]:
        """Get experience flow over time"""
        experiences = list(self.experiences.values())
        experiences.sort(key=lambda x: x.tick)
        
        if not experiences:
            return []
        
        min_tick = experiences[0].tick
        max_tick = experiences[-1].tick
        
        flow = []
        current_tick = min_tick
        
        while current_tick <= max_tick:
            window_exps = [
                exp for exp in experiences
                if current_tick <= exp.tick < current_tick + window_size
            ]
            
            if window_exps:
                avg_quality = sum(exp.processing_quality for exp in window_exps) / len(window_exps)
                
                flow.append({
                    "tick_range": (current_tick, current_tick + window_size - 1),
                    "experience_count": len(window_exps),
                    "average_quality": round(avg_quality, 3),
                    "types": {}
                })
                
                # Count by type
                for exp in window_exps:
                    exp_type = exp.experience_data.get("type", "unknown")
                    flow[-1]["types"][exp_type] = flow[-1]["types"].get(exp_type, 0) + 1
            
            current_tick += window_size
        
        return flow
