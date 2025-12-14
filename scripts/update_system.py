#!/usr/bin/env python3
"""
سكريبت تحديث النظام
"""

import subprocess
import sys

def run_command(cmd):
    """تشغيل أمر"""
    print(f"⚡ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️  خطأ: {result.stderr}")
    return result.stdout

def main():
    """الوظيفة الرئيسية"""
    print("🔄 تحديث النظام")
    print("=" * 40)
    
    # تحديث git
    print("\n📥 جلب التحديثات من GitHub:")
    print(run_command("git fetch origin"))
    
    print("\n🔄 دمج التحديثات:")
    print(run_command("git pull origin main"))
    
    # تثبيت المتطلبات
    if os.path.exists("requirements.txt"):
        print("\n📦 تثبيت المتطلبات:")
        print(run_command("pip install -r requirements.txt"))
    
    # تشغيل الاختبارات
    print("\n🧪 تشغيل الاختبارات:")
    if os.path.exists("tests/"):
        print(run_command("python -m pytest tests/ -v"))
    else:
        print("⚠️  مجلد tests/ غير موجود")
    
    print("\n" + "=" * 40)
    print("✅ اكتمل التحديث!")

if __name__ == "__main__":
    import os
    main()
