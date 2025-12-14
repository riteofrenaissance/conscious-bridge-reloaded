"""
Insight Tracker
Tracks and analyzes insights generated from experiences
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class InsightRecord:
    """A recorded insight"""
    id: str
    tick: int
    experience_type: str
    significance: float  # 0.0 - 1.0
    description: str
    connections: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    referenced_count: int = 0


class InsightTracker:
    """
    Tracks and analyzes insights
    
    Features:
    - Insight categorization
    - Significance tracking
    - Connection mapping
    - Wisdom accumulation
    """
    
    def __init__(self):
        self.insights: Dict[str, InsightRecord] = {}
        self.insight_connections: Dict[str, List[str]] = {}  # insight_id -> connected_insight_ids
        self.wisdom_fragments: List[Dict] = []
        
    def record_insight(
        self,
        tick: int,
        experience_type: str,
        significance: float,
        description: str,
        tags: List[str] = None
    ) -> str:
        """Record a new insight"""
        insight_id = f"insight_{len(self.insights) + 1}"
        
        insight = InsightRecord(
            id=insight_id,
            tick=tick,
            experience_type=experience_type,
            significance=significance,
            description=description,
            tags=tags or []
        )
        
        self.insights[insight_id] = insight
        
        # Check if this is a wisdom fragment
        if significance > 0.8:
            self._add_wisdom_fragment(insight)
        
        return insight_id
    
    def _add_wisdom_fragment(self, insight: InsightRecord):
        """Add insight as wisdom fragment"""
        fragment = {
            "id": insight.id,
            "tick": insight.tick,
            "significance": insight.significance,
            "description": insight.description,
            "experience_type": insight.experience_type,
            "timestamp": insight.timestamp.isoformat(),
            "tags": insight.tags.copy()
        }
        
        self.wisdom_fragments.append(fragment)
        
        # Keep only the most significant fragments
        self.wisdom_fragments.sort(key=lambda x: x["significance"], reverse=True)
        if len(self.wisdom_fragments) > 100:
            self.wisdom_fragments = self.wisdom_fragments[:100]
    
    def connect_insights(self, insight_id_1: str, insight_id_2: str, connection_strength: float = 0.5):
        """Connect two insights"""
        if insight_id_1 in self.insights and insight_id_2 in self.insights:
            # Add connection from insight 1 to insight 2
            if insight_id_1 not in self.insight_connections:
                self.insight_connections[insight_id_1] = []
            
            if insight_id_2 not in self.insight_connections[insight_id_1]:
                self.insight_connections[insight_id_1].append(insight_id_2)
            
            # Add reverse connection
            if insight_id_2 not in self.insight_connections:
                self.insight_connections[insight_id_2] = []
            
            if insight_id_1 not in self.insight_connections[insight_id_2]:
                self.insight_connections[insight_id_2].append(insight_id_1)
            
            # Tag insights as connected
            self.insights[insight_id_1].tags.append(f"connected_to:{insight_id_2}")
            self.insights[insight_id_2].tags.append(f"connected_to:{insight_id_1}")
    
    def get_insight(self, insight_id: str) -> Optional[InsightRecord]:
        """Get an insight by ID"""
        if insight_id in self.insights:
            insight = self.insights[insight_id]
            insight.referenced_count += 1
            return insight
        return None
    
    def get_connected_insights(self, insight_id: str) -> List[InsightRecord]:
        """Get insights connected to a given insight"""
        if insight_id not in self.insight_connections:
            return []
        
        connected_ids = self.insight_connections[insight_id]
        connected = []
        
        for conn_id in connected_ids:
            insight = self.get_insight(conn_id)
            if insight:
                connected.append(insight)
        
        return connected
    
    def get_insights_by_significance(self, min_significance: float = 0.0) -> List[InsightRecord]:
        """Get insights with minimum significance"""
        insights = list(self.insights.values())
        return [insight for insight in insights if insight.significance >= min_significance]
    
    def get_insights_by_type(self, experience_type: str) -> List[InsightRecord]:
        """Get insights by experience type"""
        insights = list(self.insights.values())
        return [insight for insight in insights if insight.experience_type == experience_type]
    
    def find_insight_clusters(self) -> List[List[str]]:
        """Find clusters of connected insights"""
        visited = set()
        clusters = []
        
        for insight_id in self.insights:
            if insight_id not in visited:
                cluster = self._dfs_cluster(insight_id, visited)
                if len(cluster) > 1:  # Only include clusters with multiple insights
                    clusters.append(cluster)
        
        return clusters
    
    def _dfs_cluster(self, start_id: str, visited: set) -> List[str]:
        """Depth-first search for insight cluster"""
        stack = [start_id]
        cluster = []
        
        while stack:
            current_id = stack.pop()
            if current_id not in visited:
                visited.add(current_id)
                cluster.append(current_id)
                
                # Add connected insights to stack
                if current_id in self.insight_connections:
                    for neighbor_id in self.insight_connections[current_id]:
                        if neighbor_id not in visited:
                            stack.append(neighbor_id)
        
        return cluster
    
    def get_wisdom_level(self) -> float:
        """Calculate wisdom level based on insights"""
        if not self.insights:
            return 0.0
        
        # Wisdom is based on:
        # 1. Number of high-significance insights
        # 2. Number of connections between insights
        # 3. Number of wisdom fragments
        
        high_significance = sum(1 for i in self.insights.values() if i.significance > 0.7)
        total_connections = sum(len(conns) for conns in self.insight_connections.values())
        total_fragments = len(self.wisdom_fragments)
        
        # Normalize
        wisdom_score = (
            (high_significance / max(len(self.insights), 1)) * 0.4 +
            (min(total_connections / max(len(self.insights), 1), 5) / 5) * 0.3 +
            (min(total_fragments, 20) / 20) * 0.3
        )
        
        return round(wisdom_score, 3)
    
    def get_stats(self) -> Dict:
        """Get insight tracker statistics"""
        total_insights = len(self.insights)
        
        if total_insights == 0:
            return {
                "total_insights": 0,
                "wisdom_level": 0.0
            }
        
        # Calculate average significance
        avg_significance = sum(i.significance for i in self.insights.values()) / total_insights
        
        # Count by type
        type_counts = {}
        for insight in self.insights.values():
            type_counts[insight.experience_type] = type_counts.get(insight.experience_type, 0) + 1
        
        # Count connections
        total_connections = sum(len(conns) for conns in self.insight_connections.values())
        
        return {
            "total_insights": total_insights,
            "average_significance": round(avg_significance, 3),
            "wisdom_level": self.get_wisdom_level(),
            "wisdom_fragments": len(self.wisdom_fragments),
            "insight_types": type_counts,
            "total_connections": total_connections,
            "insight_clusters": len(self.find_insight_clusters())
        }
