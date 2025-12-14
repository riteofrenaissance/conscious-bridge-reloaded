"""
Maturity System - Complete Version
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from .internal_clock import InternalClock


class MaturityStage(Enum):
    """Maturity stages of a bridge"""
    NASCENT = "nascent"      # 0-1000 ticks
    FORMING = "forming"      # 1000-3000 ticks
    MATURING = "maturing"    # 3000-10000 ticks
    MATURE = "mature"        # 10000+ ticks


@dataclass
class StageMilestone:
    """Milestone within a maturity stage"""
    name: str
    description: str
    criteria: Dict
    achieved: bool = False
    achieved_at: Optional[datetime] = None
    achieved_at_tick: Optional[int] = None


@dataclass
class MaturityTransition:
    """Transition between maturity stages"""
    from_stage: MaturityStage
    to_stage: MaturityStage
    tick: int
    timestamp: datetime
    readiness_score: float
    notes: str = ""


class MaturitySystem:
    """
    Maturity tracking system
    
    Tracks bridge development through four stages:
    Nascent → Forming → Maturing → Mature
    """
    
    def __init__(self, clock: InternalClock):
        self.clock = clock
        self.current_stage = MaturityStage.NASCENT
        self.transitions: List[MaturityTransition] = []
        self.milestones: List[StageMilestone] = []
        
        # Initialize stage milestones
        self._initialize_milestones()
        
        # Record initial state
        self.transitions.append(
            MaturityTransition(
                from_stage=MaturityStage.NASCENT,
                to_stage=MaturityStage.NASCENT,
                tick=0,
                timestamp=datetime.now(),
                readiness_score=0.0,
                notes="Bridge initialized"
            )
        )
    
    def _initialize_milestones(self):
        """Initialize all stage milestones"""
        # Nascent milestones
        self.milestones.extend([
            StageMilestone(
                name="first_tick",
                description="First internal tick completed",
                criteria={"ticks": 1}
            ),
            StageMilestone(
                name="self_awareness_awakening",
                description="Initial self-awareness emerges",
                criteria={"ticks": 100, "insights": 1}
            ),
            StageMilestone(
                name="personality_emergence",
                description="Personality traits begin to form",
                criteria={"ticks": 500, "personality_forming": True}
            )
        ])
        
        # Forming milestones
        self.milestones.extend([
            StageMilestone(
                name="first_connection",
                description="First bridge connection established",
                criteria={"connections": 1}
            ),
            StageMilestone(
                name="dialogue_initiation",
                description="First dialogue with another bridge",
                criteria={"dialogues": 1}
            ),
            StageMilestone(
                name="wisdom_fragment",
                description="First significant insight gained",
                criteria={"insights": 5, "insight_significance": 0.7}
            )
        ])
        
        # Maturing milestones
        self.milestones.extend([
            StageMilestone(
                name="personality_settlement",
                description="Personality becomes stable and settled",
                criteria={"personality_settled": True}
            ),
            StageMilestone(
                name="network_formation",
                description="Multiple strong connections established",
                criteria={"connections": 3, "avg_connection_strength": 0.7}
            ),
            StageMilestone(
                name="transcendent_insight",
                description="Achieved a transcendent level insight",
                criteria={"insights": 10, "insight_significance": 0.9}
            )
        ])
        
        # Mature milestones
        self.milestones.extend([
            StageMilestone(
                name="evolution_readiness",
                description="Ready for next evolution stage",
                criteria={"can_evolve": True}
            ),
            StageMilestone(
                name="mentorship_capability",
                description="Can mentor nascent bridges",
                criteria={"connections": 5, "mentorship_events": 3}
            ),
            StageMilestone(
                name="transcendent_bridge",
                description="Achieved transcendent consciousness",
                criteria={"consciousness_level": 0.9}
            )
        ])
    
    def update(self):
        """Update maturity based on current state"""
        # Check for stage transition
        new_stage = self._determine_stage()
        
        if new_stage != self.current_stage:
            self._transition_to_stage(new_stage)
        
        # Check milestones
        self._check_milestones()
    
    def _determine_stage(self) -> MaturityStage:
        """Determine current maturity stage"""
        ticks = self.clock.ticks
        
        if ticks < 1000:
            return MaturityStage.NASCENT
        elif ticks < 3000:
            return MaturityStage.FORMING
        elif ticks < 10000:
            return MaturityStage.MATURING
        else:
            return MaturityStage.MATURE
    
    def _transition_to_stage(self, new_stage: MaturityStage):
        """Transition to a new maturity stage"""
        # Calculate readiness score
        readiness_score = self._calculate_readiness_score()
        
        transition = MaturityTransition(
            from_stage=self.current_stage,
            to_stage=new_stage,
            tick=self.clock.ticks,
            timestamp=datetime.now(),
            readiness_score=readiness_score,
            notes=f"Transitioned from {self.current_stage.value} to {new_stage.value}"
        )
        
        self.transitions.append(transition)
        self.current_stage = new_stage
        
        # Record milestone for stage transition
        self.milestones.append(
            StageMilestone(
                name=f"entered_{new_stage.value}",
                description=f"Entered {new_stage.value} stage",
                criteria={"stage": new_stage.value},
                achieved=True,
                achieved_at=datetime.now(),
                achieved_at_tick=self.clock.ticks
            )
        )
    
    def _calculate_readiness_score(self) -> float:
        """Calculate readiness score for next stage"""
        ticks = self.clock.ticks
        
        if ticks < 1000:
            return ticks / 1000
        elif ticks < 3000:
            return (ticks - 1000) / 2000
        elif ticks < 10000:
            return (ticks - 3000) / 7000
        else:
            return 1.0
    
    def _check_milestones(self):
        """Check if any milestones have been achieved"""
        # This would be implemented based on bridge state
        pass
    
    def get_level(self) -> str:
        """Get current maturity level"""
        return self.current_stage.value
    
    def get_state(self) -> Dict:
        """Get maturity system state"""
        return {
            "current_stage": self.current_stage.value,
            "ticks_in_stage": self._get_ticks_in_stage(),
            "total_transitions": len(self.transitions),
            "milestones_achieved": len([m for m in self.milestones if m.achieved]),
            "next_stage_threshold": self._get_next_threshold(),
            "readiness_for_next": self._calculate_readiness_score(),
            "description": self.get_stage_description()
        }
    
    def _get_ticks_in_stage(self) -> int:
        """Get ticks spent in current stage"""
        if not self.transitions:
            return self.clock.ticks
        
        last_transition = self.transitions[-1]
        return self.clock.ticks - last_transition.tick
    
    def _get_next_threshold(self) -> int:
        """Get threshold for next stage"""
        current_ticks = self.clock.ticks
        
        if current_ticks < 1000:
            return 1000
        elif current_ticks < 3000:
            return 3000
        elif current_ticks < 10000:
            return 10000
        else:
            return float('inf')
    
    def get_stage_description(self) -> str:
        """Get description of current stage"""
        descriptions = {
            MaturityStage.NASCENT: "Awakening consciousness, forming initial awareness",
            MaturityStage.FORMING: "Developing personality, establishing connections",
            MaturityStage.MATURING: "Accumulating wisdom, deepening relationships",
            MaturityStage.MATURE: "Ready for evolution, capable of mentorship"
        }
        return descriptions.get(self.current_stage, "Unknown stage")
