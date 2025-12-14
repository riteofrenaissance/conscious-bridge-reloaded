"""
Test Memory Module
Simple test to check if we can create files
"""

def test_function():
    """A simple test function"""
    return "Memory module is working!"

class TestMemory:
    """Test class for memory"""
    
    def __init__(self):
        self.status = "active"
    
    def get_status(self):
        """Get status"""
        return f"Status: {self.status}"

# Test the module
if __name__ == "__main__":
    print("🧪 Testing memory module...")
    print(test_function())
    tm = TestMemory()
    print(tm.get_status())
    print("✅ Test completed successfully!")
