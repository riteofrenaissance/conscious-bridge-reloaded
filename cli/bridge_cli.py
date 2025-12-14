#!/usr/bin/env python3
"""
CLI متقدم لإدارة Conscious Bridge
"""

import sys
import os
import click

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@click.group()
def cli():
    """Conscious Bridge Reloaded - إدارة النظام"""
    click.echo("🧠 Conscious Bridge Reloaded v2.1.0")
    click.echo("=" * 50)

@cli.command()
def status():
    """عرض حالة النظام"""
    click.echo("📊 حالة النظام:")
    
    # التحقق من المكونات
    components = [
        ("evolution", "النظام التطوري"),
        ("core", "النواة الأساسية"),
        ("api", "واجهة API"),
        ("scripts", "السكريبتات"),
        ("cli", "واجهة الأوامر")
    ]
    
    for folder, name in components:
        if os.path.exists(folder):
            files = len([f for f in os.listdir(folder) if f.endswith('.py')])
            click.echo(f"  ✅ {name}: {files} ملف بايثون")
        else:
            click.echo(f"  ❌ {name}: مفقود")

@cli.command()
@click.argument('script_name')
def run(script_name):
    """تشغيل سكريبت"""
    script_path = f"scripts/{script_name}"
    
    if os.path.exists(script_path):
        click.echo(f"🚀 تشغيل: {script_name}")
        os.system(f"python {script_path}")
    else:
        click.echo(f"❌ السكريبت غير موجود: {script_name}")

@cli.command()
def test():
    """اختبار الأنظمة"""
    click.echo("🧪 اختبار الأنظمة التطورية...")
    
    try:
        # محاولة استيراد الأنظمة
        import importlib
        
        systems = [
            ("evolution.adaptation_manager", "ConsciousnessSimulator", "نظام الوعي"),
            ("evolution.adaptation_manager", "QuantumIntegrator", "النظام الكمي"),
            ("evolution.adaptation_manager", "AdvancedAnalytics", "التحليلات")
        ]
        
        for module_name, class_name, description in systems:
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, class_name):
                    click.echo(f"  ✅ {description}: جاهز")
                else:
                    click.echo(f"  ❌ {description}: غير موجود")
            except ImportError:
                click.echo(f"  ❌ {description}: خطأ استيراد")
                
    except Exception as e:
        click.echo(f"⚠️  خطأ: {e}")

@cli.command()
def update():
    """تحديث النظام من GitHub"""
    click.echo("🔄 تحديث من GitHub...")
    os.system("git pull origin main")
    click.echo("✅ تم التحديث")

if __name__ == "__main__":
    cli()
