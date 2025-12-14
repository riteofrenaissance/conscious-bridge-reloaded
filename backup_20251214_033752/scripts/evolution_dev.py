#!/usr/bin/env python3
"""
سكريبت تطوير النظام التطوري
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def main():
    """الوظيفة الرئيسية"""
    print("🧬 سكريبت التطوير التطوري")
    print("=" * 40)
    
    # التحقق من هيكل المشروع
    required_folders = ['evolution', 'core', 'api', 'memory']
    
    for folder in required_folders:
        if os.path.exists(folder):
            print(f"✅ {folder}/ - موجود")
        else:
            print(f"❌ {folder}/ - مفقود")
    
    print("\n📁 هيكل evolution/:")
    if os.path.exists("evolution"):
        for root, dirs, files in os.walk("evolution"):
            level = root.replace("evolution", "").count(os.sep)
            indent = " " * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in files[:5]:  # أول 5 ملفات فقط
                print(f"{subindent}{file}")
    
    print("\n🚀 جاهز للتطوير التطوري!")

if __name__ == "__main__":
    main()
