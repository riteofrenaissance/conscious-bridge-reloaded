#!/usr/bin/env python3
"""
تشغيل الأنظمة التطورية من مجلد evolution/
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_evolution_systems():
    """تشغيل جميع الأنظمة التطورية"""
    print("🧬 تشغيل الأنظمة التطورية")
    print("=" * 50)
    
    # التحقق من وجود evolution/
    if not os.path.exists("evolution"):
        print("❌ مجلد evolution/ غير موجود")
        return
    
    # استيراد الأنظمة من evolution/
    systems = []
    
    try:
        from evolution.adaptation_manager import (
            ConsciousnessSimulator,
            QuantumIntegrator,
            AdvancedAnalytics,
            MonitoringSystem
        )
        systems.extend([
            ("ConsciousnessSimulator", ConsciousnessSimulator),
            ("QuantumIntegrator", QuantumIntegrator),
            ("AdvancedAnalytics", AdvancedAnalytics),
            ("MonitoringSystem", MonitoringSystem)
        ])
        print("✅ تم استيراد الأنظمة من adaptation_manager.py")
    except ImportError as e:
        print(f"⚠️  خطأ في الاستيراد: {e}")
    
    # تشغيل كل نظام
    print("\n🚀 تشغيل الأنظمة:")
    for name, SystemClass in systems:
        try:
            system = SystemClass()
            print(f"\n  🔸 {name}:")
            
            # اختبار بسيط لكل نظام
            if hasattr(system, '__init__'):
                print(f"    ✅ تم التهيئة")
            
            # استدعاء دالة إن وجدت
            test_methods = ['simulate_conscious_adaptation', 'quantum_integrate', 
                          'get_advanced_insights', 'monitor_metric']
            
            for method in test_methods:
                if hasattr(system, method):
                    try:
                        result = getattr(system, method)({})
                        print(f"    ✅ {method}: نجح")
                    except:
                        print(f"    ⚠️  {method}: خطأ في التشغيل")
                        continue
            
        except Exception as e:
            print(f"    ❌ {name}: {str(e)[:50]}")
    
    print("\n" + "=" * 50)
    print(f"✅ اكتمل تشغيل {len(systems)} أنظمة")

if __name__ == "__main__":
    run_evolution_systems()
