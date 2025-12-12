"""
Conscious Bridge Reloaded API - Working Minimal Version
"""

from flask import Flask, jsonify, request
from datetime import datetime
import random

# Initialize Flask
app = Flask(__name__)

# Simple Bridge Class
class ConsciousBridge:
    """Minimal bridge class"""
    
    def __init__(self, bridge_id: str, name: str, bridge_type: str = "philosophical"):
        self.id = bridge_id
        self.name = name
        self.type = bridge_type
        self.created_at = datetime.now()
        
        # Core systems
        self.ticks = 0
        self.awareness = 0.1
        self.birth_time = datetime.now()
        
        # Memory
        self.experiences = []
        self.insights = []
        
        # State
        self.is_active = True
    
    def tick(self):
        """Process one tick"""
        self.ticks += 1
        self.awareness = min(1.0, self.awareness + 0.001)
        
        # Occasionally generate insight
        if self.ticks % 10 == 0:
            insight = {
                "tick": self.ticks,
                "type": "spontaneous",
                "description": f"Insight at tick {self.ticks}",
                "significance": random.uniform(0.1, 0.5)
            }
            self.insights.append(insight)
        
        return self.ticks
    
    def add_experience(self, experience_data: dict):
        """Add an experience"""
        exp = {
            "tick": self.ticks,
            "data": experience_data,
            "timestamp": datetime.now()
        }
        self.experiences.append(exp)
        
        # Process experience
        if random.random() < 0.3:
            insight = {
                "tick": self.ticks,
                "type": "from_experience",
                "description": f"Learned from: {experience_data.get('type', 'unknown')}",
                "significance": random.uniform(0.2, 0.8)
            }
            self.insights.append(insight)
    
    def get_state(self):
        """Get bridge state"""
        from datetime import datetime
        age_seconds = (datetime.now() - self.birth_time).total_seconds()
        time_ratio = self.ticks / max(1, age_seconds)
        
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
            "clock": {
                "ticks": self.ticks,
                "awareness": round(self.awareness, 3),
                "age_seconds": round(age_seconds, 2),
                "time_ratio": round(time_ratio, 2)
            },
            "memory": {
                "experiences": len(self.experiences),
                "insights": len(self.insights)
            },
            "consciousness": round(self.awareness, 3)
        }
    
    def get_summary(self):
        """Get summary"""
        return f"{self.name} ({self.type}) - {self.ticks} ticks - Consciousness: {self.awareness:.3f}"

# In-memory storage
bridges = {}
bridge_counter = 1

@app.route('/')
def index():
    """Home page"""
    bridges_html = ""
    for bridge in bridges.values():
        bridges_html += f'<div class="bridge">{bridge.get_summary()}</div>'
    
    html = f'''
    <html>
    <head>
        <title>Conscious Bridge Reloaded</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .bridge {{ background: #f5f5f5; padding: 20px; margin: 10px 0; border-radius: 5px; }}
            .method {{ font-weight: bold; color: #007bff; }}
            .endpoint {{ background: #e9ecef; padding: 10px; margin: 5px 0; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <h1>🌉 Conscious Bridge Reloaded</h1>
        <p><strong>Bridges Active:</strong> {len(bridges)}</p>
        
        <h2>Active Bridges:</h2>
        {bridges_html}
        
        <h2>API Endpoints:</h2>
        <div class="endpoint">
            <span class="method">GET</span> /api/bridges - List bridges
        </div>
        <div class="endpoint">
            <span class="method">POST</span> /api/bridges - Create bridge
        </div>
        <div class="endpoint">
            <span class="method">POST</span> /api/bridges/&lt;id&gt;/tick - Process tick
        </div>
        <div class="endpoint">
            <span class="method">GET</span> /api/bridges/&lt;id&gt;/state - Get bridge state
        </div>
        <div class="endpoint">
            <span class="method">GET</span> /api/health - Health check
        </div>
    </body>
    </html>
    '''
    return html

@app.route('/api/bridges', methods=['GET'])
def list_bridges():
    """List all bridges"""
    bridge_list = [bridge.get_state() for bridge in bridges.values()]
    return jsonify({
        "count": len(bridge_list),
        "bridges": bridge_list,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/bridges', methods=['POST'])
def create_bridge():
    """Create a new bridge"""
    global bridge_counter
    
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    # Generate ID
    bridge_id = f"bridge_{bridge_counter}"
    bridge_counter += 1
    
    # Create bridge
    bridge = ConsciousBridge(
        bridge_id=bridge_id,
        name=data['name'],
        bridge_type=data.get('type', 'philosophical')
    )
    
    # Store bridge
    bridges[bridge_id] = bridge
    
    return jsonify({
        "message": "Bridge created successfully",
        "bridge": bridge.get_state()
    }), 201

@app.route('/api/bridges/<bridge_id>/tick', methods=['POST'])
def process_tick(bridge_id):
    """Process a tick for a bridge"""
    if bridge_id not in bridges:
        return jsonify({"error": "Bridge not found"}), 404
    
    bridge = bridges[bridge_id]
    tick_number = bridge.tick()
    
    return jsonify({
        "message": f"Tick processed for {bridge.name}",
        "tick_number": tick_number,
        "bridge_state": bridge.get_state()
    })

@app.route('/api/bridges/<bridge_id>/state', methods=['GET'])
def get_bridge_state(bridge_id):
    """Get bridge state"""
    if bridge_id not in bridges:
        return jsonify({"error": "Bridge not found"}), 404
    
    return jsonify(bridges[bridge_id].get_state())

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "bridges_count": len(bridges),
        "system": "Conscious Bridge Reloaded Minimal"
    })

if __name__ == '__main__':
    print("="*60)
    print("🚀 Conscious Bridge Reloaded - Minimal Version")
    print("="*60)
    print("🌐 Starting server on http://localhost:5000")
    print("📚 API ready!")
    
    # Create sample bridges
    sample_bridge1 = ConsciousBridge("sample_1", "Wisdom-Seeker", "philosophical")
    sample_bridge2 = ConsciousBridge("sample_2", "Science-Explorer", "scientific")
    bridges["sample_1"] = sample_bridge1
    bridges["sample_2"] = sample_bridge2
    
    print(f"✅ Created 2 sample bridges")
    print("👉 Access at: http://localhost:5000")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
