"""
أدوات مساعدة لـ CLI
"""

import os
import sys
import datetime

def show_version():
    """عرض إصدار النظام"""
    print("🧠 Conscious Bridge Reloaded v2.1.0")
    print("📅 تم إنشاء CLI في:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def check_system():
    """فحص شامل للنظام"""
    print("🔍 فحص النظام الشامل...")
    print("=" * 40)
    
    # المجلدات الأساسية
    folders = [
        ("evolution", "النظام التطوري"),
        ("core", "النواة الأساسية"),
        ("api", "واجهة API"),
        ("scripts", "السكريبتات"),
        ("cli", "واجهة الأوامر"),
        ("memory", "نظام الذاكرة"),
        ("config", "الإعدادات"),
        ("docs", "التوثيق")
    ]
    
    for folder, description in folders:
        if os.path.exists(folder):
            # حساب عدد الملفات
            files_count = 0
            size_kb = 0
            
            for root, dirs, files in os.walk(folder):
                files_count += len(files)
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        size_kb += os.path.getsize(file_path) / 1024
                    except:
                        pass
            
            print(f"✅ {description} ({folder}/)")
            print(f"   📄 الملفات: {files_count}")
            print(f"   📦 الحجم: {size_kb:.1f} KB")
        else:
            print(f"❌ {description} ({folder}/): مفقود")

def list_scripts():
    """عرض السكريبتات المتاحة"""
    print("📜 السكريبتات المتاحة في scripts/:")
    print("=" * 40)
    
    if os.path.exists("scripts"):
        scripts = os.listdir("scripts")
        python_scripts = [s for s in scripts if s.endswith('.py')]
        shell_scripts = [s for s in scripts if s.endswith('.sh')]
        
        if python_scripts:
            print("🐍 ملفات Python:")
            for script in sorted(python_scripts):
                path = os.path.join("scripts", script)
                size = os.path.getsize(path) if os.path.exists(path) else 0
                print(f"   • {script} ({size} بايت)")
        
        if shell_scripts:
            print("🐚 ملفات Shell:")
            for script in sorted(shell_scripts):
                path = os.path.join("scripts", script)
                size = os.path.getsize(path) if os.path.exists(path) else 0
                print(f"   • {script} ({size} بايت)")
        
        print(f"\n📊 الإجمالي: {len(python_scripts)} Python, {len(shell_scripts)} Shell")
    else:
        print("❌ مجلد scripts/ غير موجود")

def get_project_info():
    """الحصول على معلومات المشروع"""
    info = {
        "name": "Conscious Bridge Reloaded",
        "version": "2.1.0",
        "path": os.getcwd(),
        "python_version": sys.version.split()[0],
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    # إضافة معلومات Git إذا كان متاحاً
    try:
        import subprocess
        git_branch = subprocess.check_output(["git", "branch", "--show-current"], 
                                           text=True).strip()
        git_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], 
                                           text=True).strip()
        info["git_branch"] = git_branch
        info["git_commit"] = git_commit
    except:
        info["git_branch"] = "غير متاح"
        info["git_commit"] = "غير متاح"
    
    return info

def print_project_info():
    """طباعة معلومات المشروع"""
    info = get_project_info()
    
    print("📋 معلومات المشروع:")
    print("=" * 40)
    
    for key, value in info.items():
        if key == "name":
            print(f"🏷️  الاسم: {value}")
        elif key == "version":
            print(f"📦 الإصدار: {value}")
        elif key == "path":
            print(f"📁 المسار: {value}")
        elif key == "python_version":
            print(f"🐍 Python: {value}")
        elif key == "git_branch":
            print(f"🌿 فرع Git: {value}")
        elif key == "git_commit":
            print(f"🔗 Commit: {value}")
        elif key == "timestamp":
            print(f"🕒 الوقت: {value}")
    
    print("=" * 40)

def quick_check():
    """فحص سريع"""
    print("⚡ فحص سريع للنظام...")
    
    checks = [
        ("📁 evolution/", os.path.exists("evolution")),
        ("📁 core/", os.path.exists("core")),
        ("📁 scripts/", os.path.exists("scripts")),
        ("📁 cli/", os.path.exists("cli")),
        ("📄 README.md", os.path.exists("README.md")),
        ("📄 requirements.txt", os.path.exists("requirements.txt")),
        ("🔧 .git/", os.path.exists(".git"))
    ]
    
    passed = 0
    total = len(checks)
    
    for name, exists in checks:
        if exists:
            print(f"✅ {name}")
            passed += 1
        else:
            print(f"❌ {name}")
    
    print(f"\n📊 النتيجة: {passed}/{total} ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("🎉 النظام جاهز تماماً!")
    elif passed >= total * 0.8:
        print("👍 النظام جاهز بشكل عام")
    else:
        print("⚠️  النظام يحتاج إصلاحات")

if __name__ == "__main__":
    # تشغيل عند تنفيذ الملف مباشرة
    show_version()
    print()
    quick_check()
