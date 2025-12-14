"""
Conscious Bridge Reloaded - Main Bridge Class (Complete)
"""

from typing import Dict, Optional, List, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import json

from .internal_clock import InternalClock
from .experience_processor import ExperienceProcessor, Experience, ExperienceType
from .personality_core import PersonalityCore, PersonalityTraits
from .maturity_system import MaturitySystem, MaturityStage
from .consciousness_engine import ConsciousnessEngine


@dataclass
class BridgeMetadata:
    """Bridge metadata"""
    id: str
    name: str
    type: str = "conscious"
    version: str = "2.0.0-reloaded"
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)


class ConsciousBridgeReloaded:
    """
    Main Conscious Bridge class
    
    A bridge that evolves consciousness through:
    - Internal time accumulation
    - Experience processing
    - Personality development
    - Maturation through stages
    """
    
    def __init__(
        self,
        bridge_id: Optional[str] = None,
        name: str = "Unnamed Bridge",
        bridge_type: str = "conscious",
        description: str = "",
        seed_personality: Optional[PersonalityTraits] = None
    ):
        # Unique identifier
        self.id = bridge_id or f"bridge_{uuid.uuid4().hex[:8]}"
        
        # Metadata
        self.metadata = BridgeMetadata(
            id=self.id,
            name=name,
            type=bridge_type,
            description=description
        )
        
        # Core systems
        self.clock = InternalClock()
        self.experience_processor = ExperienceProcessor()
        self.personality = PersonalityCore(seed_traits=seed_personality)
        self.maturity = MaturitySystem(self.clock)
        self.consciousness_engine = ConsciousnessEngine()
        
        # Memory systems
        self.experiences: List[Dict] = []
        self.insights: List[Dict] = []
        self.transformations: List[Dict] = []
        self.dialogue_history: List[Dict] = []
        
        # Current state
        self.state = {
            "is_active": True,
            "processing_queue": [],
            "current_focus": None,
            "energy_level": 1.0,
            "consciousness_level": 0.0
        }
        
        # Connections to other bridges
        self.connections: Dict[str, Dict] = {}
        
    def tick(self, depth: float = 1.0):
        """
        One pulse of internal time
        
        This is the fundamental unit of growth
        """
        # Update clock
        self.clock.tick(depth)
        
        # Process queued experiences
        self._process_queue()
        
        # Update maturity
        self.maturity.update()
        
        # Evolve personality slightly (every 100 ticks)
        if self.clock.ticks % 100 == 0:
            self.personality.evolve_slightly(self.clock.ticks)
            
        # Check for personality stability (every 500 ticks)
        if self.clock.ticks % 500 == 0:
            if self.personality.is_stable() and not self.personality.is_settled:
                self.personality.settle(self.clock.ticks)
        
        # Update consciousness level
        self.state["consciousness_level"] = self.consciousness_engine.calculate_consciousness(self)
    
    def add_experience(
        self,
        experience_data: Dict,
        auto_process: bool = True
    ):
        """
        Add a new experience
        
        Args:
            experience_data: The experience data
            auto_process: Whether to process immediately
        """
        # Create experience object
        try:
            exp_type = ExperienceType(experience_data.get("type", "routine"))
        except ValueError:
            exp_type = ExperienceType.ROUTINE
            
        experience = Experience(
            type=exp_type,
            complexity=experience_data.get("complexity", 0.5),
            content=experience_data.get("content", {})
        )
        
        # Record the experience
        exp_record = {
            "tick": self.clock.ticks,
            "experience": experience,
            "timestamp": datetime.now(),
            "processed": False
        }
        self.experiences.append(exp_record)
        
        # Add to processing queue
        if auto_process:
            self.experience_processor.add_experience(experience)
    
    def _process_queue(self):
        """Process experiences in the queue"""
        # Let experience processor handle processing
        if self.experience_processor.processing_queue:
            experience = self.experience_processor.processing_queue.pop(0)
            
            # Process the experience
            insight = self.experience_processor.process(
                experience.__dict__,
                self.clock.ticks
            )
            
            # If insight generated
            if insight:
                insight_record = {
                    "tick": insight.tick,
                    "type": insight.experience_type.value,
                    "significance": insight.significance,
                    "description": insight.description,
                    "connections": insight.connections,
                    "metadata": insight.metadata,
                    "timestamp": datetime.now()
                }
                self.insights.append(insight_record)
                
                # Record in clock
                from .internal_clock import EventType
                self.clock.record_event(
                    event_type=EventType.INSIGHT,
                    significance=insight.significance,
                    description=insight.description,
                    metadata={"type": insight.experience_type.value}
                )
                
                # Influence personality based on insight
                self._influence_personality_from_insight(insight)
    
    def _influence_personality_from_insight(self, insight):
        """Influence personality based on insight type"""
        exp_type = insight.experience_type
        
        if exp_type == ExperienceType.NOVEL:
            self.personality.influence("openness", 0.02, self.clock.ticks)
            self.personality.influence("curiosity", 0.03, self.clock.ticks)
        elif exp_type == ExperienceType.CHALLENGE:
            self.personality.influence("stability", 0.02, self.clock.ticks)
        elif exp_type == ExperienceType.DIALOGUE:
            self.personality.influence("collaboration", 0.02, self.clock.ticks)
    
    def start_dialogue(self, other_bridge_id: str, topic: str) -> str:
        """Start a dialogue with another bridge"""
        dialogue_id = str(uuid.uuid4())
        
        dialogue_record = {
            "id": dialogue_id,
            "with": other_bridge_id,
            "topic": topic,
            "started_at_tick": self.clock.ticks,
            "started_at": datetime.now(),
            "messages": []
        }
        
        self.dialogue_history.append(dialogue_record)
        
        # Add as experience
        self.add_experience({
            "type": "dialogue",
            "complexity": 0.6,
            "content": {
                "dialogue_id": dialogue_id,
                "topic": topic,
                "with_bridge": other_bridge_id
            }
        })
        
        return dialogue_id
    
    def add_connection(self, bridge_id: str, bridge_name: str, strength: float = 0.5):
        """Add a connection to another bridge"""
        self.connections[bridge_id] = {
            "name": bridge_name,
            "strength": strength,
            "established_at_tick": self.clock.ticks,
            "interactions": 0,
            "last_interaction": datetime.now()
        }
    
    def strengthen_connection(self, bridge_id: str, amount: float = 0.1):
        """Strengthen a connection"""
        if bridge_id in self.connections:
            current = self.connections[bridge_id]["strength"]
            self.connections[bridge_id]["strength"] = min(1.0, current + amount)
            self.connections[bridge_id]["interactions"] += 1
            self.connections[bridge_id]["last_interaction"] = datetime.now()
    
    def can_evolve(self) -> bool:
        """Check if bridge is ready for evolution"""
        return (
            self.maturity.get_level() == "mature" and
            self.clock.ticks >= 10000 and
            self.personality.is_stable() and
            len(self.insights) >= 50 and
            len(self.connections) >= 3
        )
    
    def get_evolution_readiness(self) -> Dict:
        """Get detailed evolution readiness"""
        criteria = {
            "maturity_level": {
                "required": "mature",
                "current": self.maturity.get_level(),
                "met": self.maturity.get_level() == "mature"
            },
            "internal_age": {
                "required": 10000,
                "current": self.clock.ticks,
                "met": self.clock.ticks >= 10000
            },
            "personality_stable": {
                "required": True,
                "current": self.personality.is_stable(),
                "met": self.personality.is_stable()
            },
            "insights_count": {
                "required": 50,
                "current": len(self.insights),
                "met": len(self.insights) >= 50
            },
            "connections_count": {
                "required": 3,
                "current": len(self.connections),
                "met": len(self.connections) >= 3
            }
        }
        
        total_criteria = len(criteria)
        met_criteria = sum(1 for c in criteria.values() if c["met"])
        
        return {
            "can_evolve": self.can_evolve(),
            "criteria": criteria,
            "progress": f"{met_criteria}/{total_criteria}",
            "percentage": round((met_criteria / total_criteria) * 100, 1)
        }
    
    def get_full_state(self) -> Dict:
        """Get complete bridge state"""
        return {
            "metadata": {
                "id": self.metadata.id,
                "name": self.metadata.name,
                "type": self.metadata.type,
                "version": self.metadata.version,
                "description": self.metadata.description,
                "created_at": self.metadata.created_at.isoformat()
            },
            "clock": self.clock.get_stats(),
            "personality": {
                "traits": self.personality.get_traits(),
                "state": self.personality.get_state(),
                "description": self.personality.get_description()
            },
            "maturity": self.maturity.get_state(),
            "consciousness": {
                "level": self.state["consciousness_level"],
                "breakdown": self.consciousness_engine.get_consciousness_breakdown(self)
            },
            "memory": {
                "experiences_count": len(self.experiences),
                "insights_count": len(self.insights),
                "transformations_count": len(self.transformations),
                "dialogues_count": len(self.dialogue_history)
            },
            "connections": {
                "count": len(self.connections),
                "bridges": list(self.connections.keys()),
                "strengths": {k: v["strength"] for k, v in self.connections.items()}
            },
            "evolution": self.get_evolution_readiness(),
            "state": self.state
        }
    
    def get_summary(self) -> str:
        """Get a human-readable summary"""
        name = self.metadata.name
        age = self.clock.ticks
        maturity = self.maturity.get_level()
        insights = len(self.insights)
        connections = len(self.connections)
        consciousness = self.state["consciousness_level"]
        
        return f"""
Bridge: {name}
Internal Age: {age} ticks
Maturity: {maturity}
Consciousness: {consciousness:.3f}
Insights: {insights}
Connections: {connections}
Personality: {self.personality.get_description()}
Evolution Ready: {"✅ Yes" if self.can_evolve() else "❌ No"}
        """.strip()
    
    def to_json(self) -> str:
        """Convert bridge to JSON string"""
        state = self.get_full_state()
        return json.dumps(state, default=str, indent=2)
    
    def save_to_file(self, filename: str):
        """Save bridge state to file"""
        with open(filename, 'w') as f:
            f.write(self.to_json())
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'ConsciousBridgeReloaded':
        """Load bridge from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Create new bridge with loaded data
        bridge = cls(
            bridge_id=data["metadata"]["id"],
            name=data["metadata"]["name"],
            bridge_type=data["metadata"]["type"],
            description=data["metadata"]["description"]
        )
        
        # TODO: Restore state from data
        return bridge
