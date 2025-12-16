"""
Test PersonalityCore system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_personality_creation():
    """Test personality core creation"""
    from core.personality_core import PersonalityCore
    personality = PersonalityCore()
    assert personality is not None
    return True

if __name__ == "__main__":
    print("🧠 Testing PersonalityCore...")
    test_personality_creation() and print("✅ Personality core: PASS")
    print("🎉 PersonalityCore tests completed")
