#!/usr/bin/env python3
"""
فحص صحة النظام
"""

import os
import sys
import importlib

def check_imports():
    """فحص استيراد المكونات"""
    modules_to_check = [
        "evolution",
        "core",
        "api",
        "memory",
        "dialogue"
    ]
    
    results = []
    for module in modules_to_check:
        try:
            importlib.import_module(module)
            results.append((module, "✅", "مستورد"))
        except ImportError as e:
            results.append((module, "❌", f"خطأ: {str(e)[:50]}"))
    
    return results

def check_files():
    """فحص الملفات الأساسية"""
    essential_files = [
        "evolution/adaptation_manager.py",
        "core/bridge_reloaded.py",
        "api/server.py",
        "README.md",
        "requirements.txt"
    ]
    
    results = []
    for file in essential_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            results.append((file, "✅", f"{size} بايت"))
        else:
            results.append((file, "❌", "مفقود"))
    
    return results

def main():
    """الوظيفة الرئيسية"""
    print("🏥 فحص صحة النظام")
    print("=" * 50)
    
    print("\n📦 فحص الاستيراد:")
    for module, status, message in check_imports():
        print(f"  {status} {module}: {message}")
    
    print("\n📁 فحص الملفات:")
    for file, status, message in check_files():
        print(f"  {status} {file}: {message}")
    
    print("\n🔍 الإحصائيات:")
    total_py_files = sum(1 for _ in os.popen('find . -name "*.py" | grep -v __pycache__').read().strip().split('\n') if _)
    print(f"  • ملفات Python: {total_py_files}")
    
    if os.path.exists("evolution/adaptation_manager.py"):
        lines = sum(1 for _ in open("evolution/adaptation_manager.py", 'r', encoding='utf-8'))
        print(f"  • أسطر adaptation_manager.py: {lines}")
    
    print("\n" + "=" * 50)
    print("✅ اكتمل الفحص!")

if __name__ == "__main__":
    main()
