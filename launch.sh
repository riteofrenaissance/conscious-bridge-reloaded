#!/bin/bash
# إطلاق Conscious Bridge

echo "🚀 إطلاق Conscious Bridge Reloaded..."
echo "======================================"

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت"
    exit 1
fi

# خيارات التشغيل
case "$1" in
    "cli")
        echo "🖥️  تشغيل CLI..."
        python cli/command.py "${@:2}" || python cli/commands.py "${@:2}"
        ;;
    "server")
        echo "🌐 تشغيل الخادم..."
        python -m api.server
        ;;
    "test")
        echo "🧪 تشغيل الاختبارات..."
        python test_cli.py
        ;;
    "health")
        echo "🏥 فحص الصحة..."
        python scripts/health_check.py
        ;;
    *)
        echo "استخدام: $0 {cli|server|test|health}"
        echo ""
        echo "أمثلة:"
        echo "  $0 cli status"
        echo "  $0 server"
        echo "  $0 test"
        echo "  $0 health"
        ;;
esac
