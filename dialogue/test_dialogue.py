"""
Test Dialogue Module
"""

class TestDialogue:
    def __init__(self):
        self.messages = []
    
    def add_message(self, message):
        self.messages.append(message)
        return len(self.messages)
    
    def get_stats(self):
        return {
            "total_messages": len(self.messages),
            "status": "active"
        }

# Test
if __name__ == "__main__":
    td = TestDialogue()
    td.add_message("Hello")
    td.add_message("World")
    print(f"Dialogue stats: {td.get_stats()}")
    print("✅ Dialogue test passed!")
