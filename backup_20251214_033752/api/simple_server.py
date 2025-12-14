"""
Conscious Bridge Reloaded - Simple Server
"""

from flask import Flask, jsonify, request
from datetime import datetime
import random
import uuid

app = Flask(__name__)

# Simple Bridge Class
class ConsciousBridge:
    def __init__(self, name="Unnamed Bridge", bridge_type="philosophical"):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.type = bridge_type
        self.created_at = datetime.now()
        self.ticks = 0
        self.awareness = 0.1
        self.birth_time = datetime.now()
        self.experiences = []
        self.insights = []
        self.is_active = True
    
    def tick(self):
        self.ticks += 1
        self.awareness = min(1.0, self.awareness + 0.001)
        
        # Occasionally generate insight
        if random.random() < self.awareness * 0.1:
            self.insights.append({
                "tick": self.ticks,
                "description": f"Insight at tick {self.ticks}",
                "timestamp": datetime.now()
            })
        
        return self.ticks
    
    def get_maturity(self):
        if self.ticks < 1000:
            return "nascent"
        elif self.ticks < 3000:
            return "forming"
        elif self.ticks < 10000:
            return "maturing"
        else:
            return "mature"
    
    def get_state(self):
        age_seconds = (datetime.now() - self.birth_time).total_seconds()
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "created_at": self.created_at.isoformat(),
            "ticks": self.ticks,
            "awareness": round(self.awareness, 3),
            "maturity": self.get_maturity(),
            "age_seconds": round(age_seconds, 2),
            "experiences": len(self.experiences),
            "insights": len(self.insights),
            "is_active": self.is_active
        }

# Storage
bridges = {}

@app.route('/')
def home():
    html = '''<html>
<head>
    <title>Conscious Bridge</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        .bridge { background: #f0f0f0; padding: 15px; margin: 10px 0; border-radius: 5px; }
        button { padding: 8px 16px; margin: 5px; }
        input { padding: 8px; margin: 5px; }
    </style>
</head>
<body>
    <h1>Conscious Bridge Reloaded</h1>
    <p>Active Bridges: ''' + str(len(bridges)) + '''</p>
    
    <div id="bridges">Loading...</div>
    
    <h3>Create New Bridge</h3>
    <input type="text" id="bridgeName" placeholder="Bridge name">
    <button onclick="createBridge()">Create</button>
    
    <script>
    function loadBridges() {
        fetch('/api/bridges')
            .then(r => r.json())
            .then(data => {
                let html = '';
                data.bridges.forEach(b => {
                    html += '<div class="bridge">';
                    html += '<strong>' + b.name + '</strong> (' + b.type + ')<br>';
                    html += 'Ticks: ' + b.ticks + ' | Maturity: ' + b.maturity + '<br>';
                    html += 'Awareness: ' + b.awareness + '<br>';
                    html += '<button onclick="tickBridge(\'' + b.id + '\')">Tick</button>';
                    html += '<button onclick="viewBridge(\'' + b.id + '\')">View</button>';
                    html += '</div>';
                });
                document.getElementById('bridges').innerHTML = html || '<p>No bridges yet</p>';
            });
    }
    
    function createBridge() {
        const name = document.getElementById('bridgeName').value;
        
        fetch('/api/bridges', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name: name, type: 'philosophical'})
        })
        .then(r => r.json())
        .then(() => {
            document.getElementById('bridgeName').value = '';
            loadBridges();
        });
    }
    
    function tickBridge(id) {
        fetch('/api/bridges/' + id + '/tick', {method: 'POST'})
            .then(() => loadBridges());
    }
    
    function viewBridge(id) {
        window.open('/api/bridges/' + id + '/state', '_blank');
    }
    
    loadBridges();
    </script>
</body>
</html>'''
    return html

@app.route('/api/bridges', methods=['GET'])
def list_bridges():
    return jsonify({
        "count": len(bridges),
        "bridges": [b.get_state() for b in bridges.values()]
    })

@app.route('/api/bridges', methods=['POST'])
def create_bridge():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Name required"}), 400
    
    bridge = ConsciousBridge(name=data['name'], bridge_type=data.get('type', 'philosophical'))
    bridges[bridge.id] = bridge
    
    return jsonify({"message": "Created", "bridge": bridge.get_state()}), 201

@app.route('/api/bridges/<bridge_id>/tick', methods=['POST'])
def process_tick(bridge_id):
    if bridge_id not in bridges:
        return jsonify({"error": "Not found"}), 404
    
    ticks = bridges[bridge_id].tick()
    return jsonify({"message": "Tick processed", "ticks": ticks})

@app.route('/api/bridges/<bridge_id>/state', methods=['GET'])
def get_state(bridge_id):
    if bridge_id not in bridges:
        return jsonify({"error": "Not found"}), 404
    return jsonify(bridges[bridge_id].get_state())

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "bridges": len(bridges)})

if __name__ == '__main__':
    print("="*50)
    print("Conscious Bridge Reloaded - Simple Server")
    print("Server: http://localhost:5000")
    print("="*50)
    
    # Create samples
    b1 = ConsciousBridge("Wisdom-Seeker", "philosophical")
    b2 = ConsciousBridge("Science-Explorer", "scientific")
    bridges[b1.id] = b1
    bridges[b2.id] = b2
    
    for _ in range(100): b1.tick()
    for _ in range(300): b2.tick()
    
    print("Sample bridges created")
    print("="*50)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
