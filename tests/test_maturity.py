"""
Test MaturitySystem
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_maturity_creation():
    """Test maturity system creation"""
    from core.maturity_system import MaturitySystem
    from core.internal_clock import InternalClock
    
    clock = InternalClock(bridge_id="test-maturity", name="Test Clock")
    maturity = MaturitySystem(clock)
    assert maturity is not None
    return True

def test_maturity_stages():
    """Test maturity stages Enum - with ACTUAL values"""
    from core.maturity_system import MaturityStage
    
    # التحقق من القيم الفعلية
    assert hasattr(MaturityStage, 'NASCENT')
    assert hasattr(MaturityStage, 'FORMING')
    assert hasattr(MaturityStage, 'MATURING')
    assert hasattr(MaturityStage, 'MATURE')
    
    # التحقق من القيم
    assert MaturityStage.NASCENT.value == "nascent"
    assert MaturityStage.FORMING.value == "forming"
    
    print(f"   Stages: {[stage.name for stage in MaturityStage]}")
    return True

if __name__ == "__main__":
    print("🌱 Testing MaturitySystem...")
    test_maturity_creation() and print("✅ Maturity system: PASS")
    test_maturity_stages() and print("✅ Maturity stages: PASS")
    print("🎉 MaturitySystem tests completed")
