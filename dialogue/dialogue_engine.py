"""
Dialogue Engine
Handles communication between bridges
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import json


@dataclass
class DialogueMessage:
    """A message in a dialogue"""
    id: str
    sender_bridge_id: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    tick: int = 0
    metadata: Dict = field(default_factory=dict)


@dataclass
class Dialogue:
    """A dialogue between bridges"""
    id: str
    bridge_ids: List[str]
    topic: str
    messages: List[DialogueMessage] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    status: str = "active"  # active, paused, completed
    metadata: Dict = field(default_factory=dict)


class DialogueEngine:
    """
    Engine for managing dialogues between bridges
    
    Features:
    - Multi-bridge conversations
    - Topic management
    - Message routing
    - Dialogue history
    """
    
    def __init__(self):
        self.dialogues: Dict[str, Dialogue] = {}
        self.bridge_dialogues: Dict[str, List[str]] = {}  # bridge_id -> dialogue_ids
        
    def start_dialogue(self, bridge_ids: List[str], topic: str, metadata: Dict = None) -> str:
        """Start a new dialogue"""
        dialogue_id = str(uuid.uuid4())
        
        dialogue = Dialogue(
            id=dialogue_id,
            bridge_ids=bridge_ids.copy(),
            topic=topic,
            metadata=metadata or {}
        )
        
        self.dialogues[dialogue_id] = dialogue
        
        # Update bridge dialogue tracking
        for bridge_id in bridge_ids:
            if bridge_id not in self.bridge_dialogues:
                self.bridge_dialogues[bridge_id] = []
            self.bridge_dialogues[bridge_id].append(dialogue_id)
        
        return dialogue_id
    
    def add_message(self, dialogue_id: str, sender_bridge_id: str, content: str, tick: int = 0, metadata: Dict = None) -> str:
        """Add a message to a dialogue"""
        if dialogue_id not in self.dialogues:
            raise ValueError(f"Dialogue {dialogue_id} not found")
        
        if sender_bridge_id not in self.dialogues[dialogue_id].bridge_ids:
            raise ValueError(f"Bridge {sender_bridge_id} not in dialogue {dialogue_id}")
        
        message_id = str(uuid.uuid4())
        message = DialogueMessage(
            id=message_id,
            sender_bridge_id=sender_bridge_id,
            content=content,
            tick=tick,
            metadata=metadata or {}
        )
        
        self.dialogues[dialogue_id].messages.append(message)
        return message_id
    
    def get_dialogue(self, dialogue_id: str) -> Optional[Dialogue]:
        """Get a dialogue by ID"""
        return self.dialogues.get(dialogue_id)
    
    def get_bridge_dialogues(self, bridge_id: str) -> List[Dialogue]:
        """Get all dialogues for a bridge"""
        dialogue_ids = self.bridge_dialogues.get(bridge_id, [])
        dialogues = []
        
        for dialogue_id in dialogue_ids:
            dialogue = self.get_dialogue(dialogue_id)
            if dialogue:
                dialogues.append(dialogue)
        
        return dialogues
    
    def get_active_dialogues(self) -> List[Dialogue]:
        """Get all active dialogues"""
        return [d for d in self.dialogues.values() if d.status == "active"]
    
    def complete_dialogue(self, dialogue_id: str):
        """Mark a dialogue as completed"""
        if dialogue_id in self.dialogues:
            self.dialogues[dialogue_id].status = "completed"
            self.dialogues[dialogue_id].ended_at = datetime.now()
    
    def get_dialogue_stats(self, dialogue_id: str) -> Dict:
        """Get statistics for a dialogue"""
        if dialogue_id not in self.dialogues:
            return {}
        
        dialogue = self.dialogues[dialogue_id]
        
        # Count messages by bridge
        message_counts = {}
        for message in dialogue.messages:
            sender = message.sender_bridge_id
            message_counts[sender] = message_counts.get(sender, 0) + 1
        
        # Calculate duration
        if dialogue.ended_at:
            duration = (dialogue.ended_at - dialogue.started_at).total_seconds()
        else:
            duration = (datetime.now() - dialogue.started_at).total_seconds()
        
        return {
            "dialogue_id": dialogue_id,
            "topic": dialogue.topic,
            "bridge_count": len(dialogue.bridge_ids),
            "message_count": len(dialogue.messages),
            "message_counts": message_counts,
            "duration_seconds": round(duration, 2),
            "status": dialogue.status,
            "started_at": dialogue.started_at.isoformat(),
            "ended_at": dialogue.ended_at.isoformat() if dialogue.ended_at else None
        }
    
    def analyze_conversation_flow(self, dialogue_id: str) -> List[Dict]:
        """Analyze conversation flow in a dialogue"""
        if dialogue_id not in self.dialogues:
            return []
        
        dialogue = self.dialogues[dialogue_id]
        
        flow = []
        for message in dialogue.messages:
            flow.append({
                "timestamp": message.timestamp.isoformat(),
                "tick": message.tick,
                "sender": message.sender_bridge_id,
                "content_length": len(message.content),
                "word_count": len(message.content.split())
            })
        
        return flow
    
    def save_dialogue(self, dialogue_id: str, filename: str):
        """Save dialogue to file"""
        if dialogue_id not in self.dialogues:
            raise ValueError(f"Dialogue {dialogue_id} not found")
        
        dialogue = self.dialogues[dialogue_id]
        
        data = {
            "id": dialogue.id,
            "bridge_ids": dialogue.bridge_ids,
            "topic": dialogue.topic,
            "messages": [
                {
                    "id": msg.id,
                    "sender_bridge_id": msg.sender_bridge_id,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "tick": msg.tick,
                    "metadata": msg.metadata
                }
                for msg in dialogue.messages
            ],
            "started_at": dialogue.started_at.isoformat(),
            "ended_at": dialogue.ended_at.isoformat() if dialogue.ended_at else None,
            "status": dialogue.status,
            "metadata": dialogue.metadata
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_dialogue(self, filename: str) -> str:
        """Load dialogue from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Create dialogue
        dialogue = Dialogue(
            id=data["id"],
            bridge_ids=data["bridge_ids"],
            topic=data["topic"],
            started_at=datetime.fromisoformat(data["started_at"]),
            ended_at=datetime.fromisoformat(data["ended_at"]) if data.get("ended_at") else None,
            status=data["status"],
            metadata=data.get("metadata", {})
        )
        
        # Add messages
        for msg_data in data["messages"]:
            message = DialogueMessage(
                id=msg_data["id"],
                sender_bridge_id=msg_data["sender_bridge_id"],
                content=msg_data["content"],
                timestamp=datetime.fromisoformat(msg_data["timestamp"]),
                tick=msg_data.get("tick", 0),
                metadata=msg_data.get("metadata", {})
            )
            dialogue.messages.append(message)
        
        # Store dialogue
        self.dialogues[dialogue.id] = dialogue
        
        # Update bridge dialogue tracking
        for bridge_id in dialogue.bridge_ids:
            if bridge_id not in self.bridge_dialogues:
                self.bridge_dialogues[bridge_id] = []
            if dialogue.id not in self.bridge_dialogues[bridge_id]:
                self.bridge_dialogues[bridge_id].append(dialogue.id)
        
        return dialogue.id
