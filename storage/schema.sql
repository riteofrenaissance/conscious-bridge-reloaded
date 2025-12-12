-- Conscious Bridge Reloaded Database Schema
-- SQLite Schema

-- Bridges table
CREATE TABLE IF NOT EXISTS bridges (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version TEXT DEFAULT '2.0-reloaded',
    
    -- Current state
    is_active BOOLEAN DEFAULT 1,
    internal_ticks INTEGER DEFAULT 0,
    maturity_level TEXT DEFAULT 'nascent',
    consciousness_level REAL DEFAULT 0.0,
    
    -- Personality traits
    trait_openness REAL DEFAULT 0.5,
    trait_stability REAL DEFAULT 0.5,
    trait_curiosity REAL DEFAULT 0.5,
    trait_collaboration REAL DEFAULT 0.5,
    
    -- Flags
    personality_forming BOOLEAN DEFAULT 0,
    personality_settled BOOLEAN DEFAULT 0,
    
    -- Counts
    experiences_count INTEGER DEFAULT 0,
    insights_count INTEGER DEFAULT 0,
    connections_count INTEGER DEFAULT 0,
    
    -- JSON data
    metadata_json TEXT,
    state_json TEXT,
    
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clock events table
CREATE TABLE IF NOT EXISTS clock_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bridge_id TEXT NOT NULL,
    tick INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    significance REAL NOT NULL,
    description TEXT,
    metadata_json TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (bridge_id) REFERENCES bridges(id) ON DELETE CASCADE
);

-- Experiences table
CREATE TABLE IF NOT EXISTS experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bridge_id TEXT NOT NULL,
    tick INTEGER NOT NULL,
    experience_type TEXT NOT NULL,
    complexity REAL NOT NULL,
    quality TEXT,
    content_json TEXT,
    processed BOOLEAN DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (bridge_id) REFERENCES bridges(id) ON DELETE CASCADE
);

-- Insights table
CREATE TABLE IF NOT EXISTS insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bridge_id TEXT NOT NULL,
    tick INTEGER NOT NULL,
    experience_type TEXT NOT NULL,
    significance REAL NOT NULL,
    description TEXT,
    connections_json TEXT,
    metadata_json TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (bridge_id) REFERENCES bridges(id) ON DELETE CASCADE
);

-- Personality snapshots table
CREATE TABLE IF NOT EXISTS personality_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bridge_id TEXT NOT NULL,
    tick INTEGER NOT NULL,
    openness REAL NOT NULL,
    stability REAL NOT NULL,
    curiosity REAL NOT NULL,
    collaboration REAL NOT NULL,
    notes TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (bridge_id) REFERENCES bridges(id) ON DELETE CASCADE
);

-- Maturity transitions table
CREATE TABLE IF NOT EXISTS maturity_transitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bridge_id TEXT NOT NULL,
    from_stage TEXT NOT NULL,
    to_stage TEXT NOT NULL,
    tick INTEGER NOT NULL,
    readiness_score REAL NOT NULL,
    notes TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (bridge_id) REFERENCES bridges(id) ON DELETE CASCADE
);

-- Connections table
CREATE TABLE IF NOT EXISTS connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bridge_id_1 TEXT NOT NULL,
    bridge_id_2 TEXT NOT NULL,
    strength REAL DEFAULT 0.5,
    established_at_tick INTEGER,
    interactions INTEGER DEFAULT 0,
    metadata_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (bridge_id_1) REFERENCES bridges(id) ON DELETE CASCADE,
    FOREIGN KEY (bridge_id_2) REFERENCES bridges(id) ON DELETE CASCADE,
    UNIQUE(bridge_id_1, bridge_id_2)
);

-- Dialogues table
CREATE TABLE IF NOT EXISTS dialogues (
    id TEXT PRIMARY KEY,
    bridge_id_1 TEXT NOT NULL,
    bridge_id_2 TEXT NOT NULL,
    topic TEXT NOT NULL,
    started_at_tick INTEGER,
    status TEXT DEFAULT 'active',
    messages_count INTEGER DEFAULT 0,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    
    FOREIGN KEY (bridge_id_1) REFERENCES bridges(id) ON DELETE CASCADE,
    FOREIGN KEY (bridge_id_2) REFERENCES bridges(id) ON DELETE CASCADE
);

-- Dialogue messages table
CREATE TABLE IF NOT EXISTS dialogue_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dialogue_id TEXT NOT NULL,
    sender_bridge_id TEXT NOT NULL,
    message TEXT NOT NULL,
    tick INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (dialogue_id) REFERENCES dialogues(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_bridge_id) REFERENCES bridges(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_bridges_maturity ON bridges(maturity_level);
CREATE INDEX IF NOT EXISTS idx_bridges_consciousness ON bridges(consciousness_level);
CREATE INDEX IF NOT EXISTS idx_clock_events_bridge ON clock_events(bridge_id, tick);
CREATE INDEX IF NOT EXISTS idx_experiences_bridge ON experiences(bridge_id, tick);
CREATE INDEX IF NOT EXISTS idx_insights_bridge ON insights(bridge_id, tick);
CREATE INDEX IF NOT EXISTS idx_connections_bridges ON connections(bridge_id_1, bridge_id_2);
CREATE INDEX IF NOT EXISTS idx_dialogues_bridges ON dialogues(bridge_id_1, bridge_id_2);