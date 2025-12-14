"""
أوامر CLI
"""

def show_version():
    print("Conscious Bridge Reloaded v2.1.0")

def check_system():
    print("🔍 فحص النظام...")
    import os
    if os.path.exists("evolution"):
        print("✅ evolution/ موجود")
    if os.path.exists("scripts"):
        print("✅ scripts/ موجود")
