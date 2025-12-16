"""
Test InternalClock system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_clock_creation():
    """Test creating an internal clock"""
    from core.internal_clock import InternalClock
    clock = InternalClock(bridge_id="test-clock", name="Test Clock")
    assert clock.name == "Test Clock"
    assert clock.bridge_id == "test-clock"
    return True

def test_temporal_event():
    """Test temporal event creation"""
    from core.internal_clock import TemporalEvent
    event = TemporalEvent("test_event", 0.75, 1234.56)
    assert event.event_type == "test_event"
    assert event.intensity == 0.75
    return True

if __name__ == "__main__":
    print("⏰ Testing InternalClock...")
    test_clock_creation() and print("✅ Clock creation: PASS")
    test_temporal_event() and print("✅ Temporal event: PASS")
    print("🎉 InternalClock tests completed")
