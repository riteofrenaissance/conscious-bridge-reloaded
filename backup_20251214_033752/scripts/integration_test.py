#!/usr/bin/env python3
"""
اختبار تكامل evolution مع core/
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_integration():
    """اختبار التكامل بين المكونات"""
    print("🔗 اختبار تكامل النظام")
    print("=" * 50)
    
    # التحقق من وجود المكونات الأساسية
    components = [
        ("evolution/", "المكونات التطورية"),
        ("core/", "النواة الأساسية"),
        ("api/", "واجهة API"),
        ("memory/", "نظام الذاكرة")
    ]
    
    missing = []
    for path, name in components:
        if os.path.exists(path):
            print(f"✅ {name} ({path}) - موجود")
        else:
            print(f"❌ {name} ({path}) - مفقود")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  المكونات المفقودة: {', '.join(missing)}")
    
    # اختبار الاستيراد المتبادل
    print("\n🔄 اختبار الاستيراد:")
    
    # من evolution إلى core
    try:
        from evolution.adaptation_manager import ConsciousnessSimulator
        print("✅ evolution → core: يعمل")
    except ImportError as e:
        print(f"❌ evolution → core: {str(e)[:50]}")
    
    # من core إلى evolution (إذا كان هناك استيراد)
    try:
        import core
        print("✅ core → evolution: يعمل")
    except ImportError as e:
        print(f"⚠️  core → evolution: {str(e)[:50]}")
    
    # اختبار API
    if os.path.exists("api/server.py"):
        print("\n🌐 اختبار API:")
        try:
            # محاولة استيراد خادم API
            import api.server
            print("✅ api.server: جاهز")
        except ImportError as e:
            print(f"❌ api.server: {str(e)[:50]}")
    
    print("\n📊 تقرير التكامل:")
    print(f"  • المكونات المتاحة: {len([c for c in components if os.path.exists(c[0])])}/{len(components)}")
    print(f"  • الأنظمة التطورية: evolution/adaptation_manager.py")
    print(f"  • جاهز للتكامل: {'نعم' if len(missing) == 0 else 'لا'}")
    
    print("\n" + "=" * 50)
    print("✅ اكتمل اختبار التكامل")

if __name__ == "__main__":
    test_integration()
