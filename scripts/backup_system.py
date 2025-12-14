#!/usr/bin/env python3
"""
نسخ احتياطي للنظام
"""

import os
import shutil
import datetime
import sys

def create_backup():
    """إنشاء نسخة احتياطية"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    
    print(f"💾 إنشاء نسخة احتياطية: {backup_dir}")
    print("=" * 50)
    
    # المجلدات التي يجب نسخها
    folders_to_backup = [
        "evolution/",
        "core/",
        "api/",
        "memory/",
        "scripts/",
        "config/"
    ]
    
    # الملفات المهمة
    files_to_backup = [
        "requirements.txt",
        "README.md",
        "setup.py",
        "LICENSE"
    ]
    
    # إنشاء مجلد النسخ الاحتياطي
    os.makedirs(backup_dir, exist_ok=True)
    
    # نسخ المجلدات
    copied_folders = 0
    for folder in folders_to_backup:
        if os.path.exists(folder):
            dest = os.path.join(backup_dir, folder)
            try:
                shutil.copytree(folder, dest, dirs_exist_ok=True)
                print(f"✅ نسخ: {folder}")
                copied_folders += 1
            except Exception as e:
                print(f"❌ خطأ في {folder}: {e}")
    
    # نسخ الملفات
    copied_files = 0
    for file in files_to_backup:
        if os.path.exists(file):
            dest = os.path.join(backup_dir, file)
            try:
                shutil.copy2(file, dest)
                print(f"✅ نسخ: {file}")
                copied_files += 1
            except Exception as e:
                print(f"❌ خطأ في {file}: {e}")
    
    # إنشاء ملف معلومات
    info_file = os.path.join(backup_dir, "BACKUP_INFO.txt")
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write(f"نسخة احتياطية - {timestamp}\n")
        f.write(f"المجلدات: {copied_folders}\n")
        f.write(f"الملفات: {copied_files}\n")
        f.write(f"المسار: {os.path.abspath(backup_dir)}\n")
    
    # حجم النسخة الاحتياطية
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(backup_dir):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    
    print("\n📊 إحصائيات النسخ الاحتياطي:")
    print(f"  • المجلدات: {copied_folders}/{len(folders_to_backup)}")
    print(f"  • الملفات: {copied_files}/{len(files_to_backup)}")
    print(f"  • الحجم: {total_size / 1024 / 1024:.2f} MB")
    print(f"  • الموقع: {backup_dir}/")
    
    print("\n" + "=" * 50)
    print("✅ اكتمل النسخ الاحتياطي!")
    
    return backup_dir

if __name__ == "__main__":
    backup_path = create_backup()
    print(f"\n🚀 للاستعادة: cp -r {backup_path}/* .")
