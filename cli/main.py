#!/usr/bin/env python3
"""
الواجهة الرئيسية لسطر الأوامر
"""

import sys
import os

def main():
    print("🧠 Conscious Bridge Reloaded CLI")
    print("=" * 40)
    print("الإصدار: 2.1.0")
    print("المسار:", os.getcwd())
    print("\nالأوامر المتاحة:")
    print("1. python cli/main.py")
    print("2. python -m cli.main")
    print("\n✅ CLI جاهز للاستخدام")

if __name__ == "__main__":
    main()
