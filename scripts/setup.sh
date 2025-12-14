#!/bin/bash
# ============================================================================
# Conscious Bridge Reloaded - سكريبت الإعداد
# الإصدار: 2.1.0
# ============================================================================

set -e  # توقف عند أول خطأ

# الألوان للطباعة
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# دالة للطباعة الملونة
print_color() {
    echo -e "${2}${1}${NC}"
}

# دالة للتحقق من الأمر
check_command() {
    if command -v $1 &> /dev/null; then
        print_color "✅ $1 مثبت" "$GREEN"
        return 0
    else
        print_color "❌ $1 غير مثبت" "$RED"
        return 1
    fi
}

# ============================================================================
# بداية الإعداد
# ============================================================================

print_color "╔══════════════════════════════════════════════════════════╗" "$BLUE"
print_color "║      Conscious Bridge Reloaded v2.1.0 - الإعداد         ║" "$BLUE"
print_color "╚══════════════════════════════════════════════════════════╝" "$BLUE"

print_color "\n📅 تاريخ التنفيذ: $(date)" "$YELLOW"
print_color "📁 المسار الحالي: $(pwd)" "$YELLOW"

# ============================================================================
# التحقق من المتطلبات الأساسية
# ============================================================================

print_color "\n🔍 التحقق من المتطلبات الأساسية..." "$BLUE"

# التحقق من Git
if check_command "git"; then
    print_color "   الإصدار: $(git --version | cut -d' ' -f3)" "$YELLOW"
fi

# التحقق من Python
if check_command "python3"; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_color "   الإصدار: $PYTHON_VERSION" "$YELLOW"
    
    # التحقق من إصدار Python
    if [[ $(echo "$PYTHON_VERSION 3.8" | awk '{print ($1 >= $2)}') -eq 1 ]]; then
        print_color "   ✓ إصدار Python مناسب" "$GREEN"
    else
        print_color "   ⚠️  إصدار Python قديم (مطلوب 3.8+)" "$RED"
    fi
fi

# التحقق من pip
if check_command "pip3"; then
    print_color "   الإصدار: $(pip3 --version | cut -d' ' -f2)" "$YELLOW"
fi

# ============================================================================
# فحص هيكل المشروع
# ============================================================================

print_color "\n🏗️  فحص هيكل المشروع..." "$BLUE"

# قائمة المجلدات الأساسية
declare -A ESSENTIAL_DIRS=(
    ["evolution"]="النظام التطوري"
    ["core"]="النواة الأساسية"
    ["api"]="واجهة البرمجة"
    ["memory"]="نظام الذاكرة"
    ["scripts"]="السكريبتات"
    ["config"]="الإعدادات"
    ["docs"]="التوثيق"
)

declare -A ESSENTIAL_FILES=(
    ["evolution/adaptation_manager.py"]="مدير التكيف"
    ["core/bridge_reloaded.py"]="الجسر الأساسي"
    ["api/server.py"]="خادم API"
    ["README.md"]="دليل الاستخدام"
    ["requirements.txt"]="المتطلبات"
    ["LICENSE"]="الترخيص"
)

# فحص المجلدات
print_color "📂 المجلدات:" "$YELLOW"
for dir in "${!ESSENTIAL_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        # حساب عدد الملفات
        file_count=$(find "$dir" -name "*.py" -type f 2>/dev/null | wc -l)
        dir_size=$(du -sh "$dir" 2>/dev/null | cut -f1)
        
        print_color "   ✓ $dir - ${ESSENTIAL_DIRS[$dir]}" "$GREEN"
        print_color "     📄 $file_count ملف بايثون | 📦 $dir_size" "$YELLOW"
    else
        print_color "   ✗ $dir - ${ESSENTIAL_DIRS[$dir]} (مفقود)" "$RED"
    fi
done

# فحص الملفات
print_color "\n📄 الملفات الأساسية:" "$YELLOW"
for file in "${!ESSENTIAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        file_size=$(wc -l < "$file" 2>/dev/null || echo "0")
        print_color "   ✓ $file - ${ESSENTIAL_FILES[$file]} ($file_size سطر)" "$GREEN"
    else
        print_color "   ✗ $file - ${ESSENTIAL_FILES[$file]} (مفقود)" "$RED"
    fi
done

# ============================================================================
# إعداد بيئة Python
# ============================================================================

print_color "\n🐍 إعداد بيئة Python..." "$BLUE"

# التحقق من وجود بيئة افتراضية
if [ -d "venv" ]; then
    print_color "   ✓ البيئة الافتراضية موجودة" "$GREEN"
    
    # تنشيط البيئة
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        print_color "   ✓ تم تنشيط البيئة" "$GREEN"
        print_color "   🎯 Python الحالي: $(which python)" "$YELLOW"
    fi
else
    print_color "   إنشاء بيئة افتراضية جديدة..." "$YELLOW"
    python3 -m venv venv
    
    if [ $? -eq 0 ]; then
        source venv/bin/activate
        print_color "   ✓ تم إنشاء وتنشيط البيئة" "$GREEN"
    else
        print_color "   ❌ فشل في إنشاء البيئة" "$RED"
        exit 1
    fi
fi

# ترقية pip
print_color "\n📦 تحديث pip..." "$YELLOW"
python -m pip install --upgrade pip
print_color "   ✓ pip محدث" "$GREEN"

# ============================================================================
# تثبيت المتطلبات
# ============================================================================

print_color "\n📋 تثبيت المتطلبات..." "$BLUE"

if [ -f "requirements.txt" ]; then
    print_color "   العثور على requirements.txt" "$YELLOW"
    req_count=$(wc -l < requirements.txt)
    print_color "   📄 $req_count حزمة مطلوبة" "$YELLOW"
    
    # تثبيت المتطلبات
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_color "   ✓ تم تثبيت جميع المتطلبات" "$GREEN"
    else
        print_color "   ⚠️  حدثت أخطاء أثناء التثبيت" "$RED"
    fi
else
    print_color "   ⚠️  ملف requirements.txt غير موجود" "$YELLOW"
    print_color "   تثبيت المتطلبات الأساسية..." "$YELLOW"
    
    # قائمة المتطلبات الأساسية
    BASIC_REQUIREMENTS="flask numpy pandas sqlalchemy python-dotenv"
    pip install $BASIC_REQUIREMENTS
    
    print_color "   ✓ تم تثبيت المتطلبات الأساسية" "$GREEN"
    
    # إنشاء ملف requirements.txt
    pip freeze > requirements.txt
    print_color "   📄 تم إنشاء requirements.txt" "$GREEN"
fi

# ============================================================================
# إعداد المجلدات الإضافية
# ============================================================================

print_color "\n📁 إنشاء المجلدات الإضافية..." "$BLUE"

declare -A ADDITIONAL_DIRS=(
    ["data"]="قاعدة البيانات"
    ["logs"]="سجلات النظام"
    ["backups"]="النسخ الاحتياطية"
    ["exports"]="التصدير"
    ["temp"]="الملفات المؤقتة"
)

for dir in "${!ADDITIONAL_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        print_color "   ✓ تم إنشاء $dir/ - ${ADDITIONAL_DIRS[$dir]}" "$GREEN"
    else
        print_color "   ✓ $dir/ موجود - ${ADDITIONAL_DIRS[$dir]}" "$YELLOW"
    fi
done

# ============================================================================
# إعداد صلاحيات السكريبتات
# ============================================================================

print_color "\n🔐 إعداد صلاحيات السكريبتات..." "$BLUE"

if [ -d "scripts" ]; then
    # جعل جميع ملفات Python قابلة للتنفيذ
    find scripts -name "*.py" -type f -exec chmod +x {} \; 2>/dev/null || true
    
    # جعل جميع ملفات Shell قابلة للتنفيذ
    find scripts -name "*.sh" -type f -exec chmod +x {} \; 2>/dev/null || true
    
    script_count=$(find scripts -name "*.py" -o -name "*.sh" | wc -l)
    print_color "   ✓ تم تعيين صلاحيات التنفيذ لـ $script_count سكريبت" "$GREEN"
    
    # عرض السكريبتات المتاحة
    print_color "\n   📜 السكريبتات المتاحة:" "$YELLOW"
    for script in scripts/*.py scripts/*.sh; do
        if [ -f "$script" ]; then
            script_name=$(basename "$script")
            if [ -x "$script" ]; then
                print_color "     ▶️  $script_name" "$GREEN"
            else
                print_color "     📄 $script_name" "$YELLOW"
            fi
        fi
    done
fi

# ============================================================================
# اختبار النظام
# ============================================================================

print_color "\n🧪 اختبار النظام..." "$BLUE"

# دالة لاختبار الاستيراد
test_import() {
    local module=$1
    local name=$2
    
    python3 -c "
import sys
sys.path.append('.')
try:
    $module
    print('   ✓ $name: نجح')
except ImportError as e:
    print('   ✗ $name: فشل -', str(e)[:40])
except Exception as e:
    print('   ⚠️  $name: خطأ -', str(e)[:40])
" 2>/dev/null
}

print_color "   اختبار استيراد المكونات:" "$YELLOW"

test_import "import evolution" "المكونات التطورية"
test_import "import core" "النواة الأساسية"
test_import "import api" "واجهة API"
test_import "from evolution.adaptation_manager import ConsciousnessSimulator" "نظام الوعي"
test_import "from core.bridge_reloaded import ConsciousBridge" "الجسر الواعي"

# ============================================================================
# إنشاء ملفات الإعداد
# ============================================================================

print_color "\n⚙️  إنشاء ملفات الإعداد..." "$BLUE"

# ملف البيئة
if [ ! -f ".env" ]; then
    cat > .env << 'ENV_FILE'
# ========================================
# إعدادات Conscious Bridge Reloaded
# ========================================

# تطبيق
APP_NAME=Conscious Bridge Reloaded
APP_VERSION=2.1.0
DEBUG=True
LOG_LEVEL=INFO

# قاعدة البيانات
DB_PATH=./data/bridges.db
DB_BACKUP_DIR=./backups

# API
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=True

# التطور
MIN_TICKS_FOR_EVOLUTION=1000
MIN_EXPERIENCES=10
EVOLUTION_READY_SCORE=0.7

# النظام التطوري
CONSCIOUSNESS_ENABLED=True
QUANTUM_INTEGRATION_ENABLED=True
ADVANCED_ANALYTICS_ENABLED=True
ENV_FILE
    
    print_color "   ✓ تم إنشاء .env" "$GREEN"
else
    print_color "   ✓ ملف .env موجود" "$YELLOW"
fi

# ملف الإعداد المحلي
if [ ! -f ".env.local" ]; then
    cat > .env.local << 'LOCAL_ENV'
# ========================================
# إعدادات محلية - لا ترفع إلى GitHub
# ========================================

# إعدادات التطوير
DEVELOPMENT_MODE=True
TEST_USER_ID=developer_001

# مسارات محلية
LOCAL_DATA_PATH=./data/local
LOG_PATH=./logs/development.log

# إعدادات اتصال (إذا لزم الأمر)
# API_KEY=your_key_here
# DATABASE_URL=sqlite:///local.db
LOCAL_ENV
    
    print_color "   ✓ تم إنشاء .env.local" "$GREEN"
    print_color "   ⚠️  ملاحظة: .env.local مضاف إلى .gitignore" "$YELLOW"
else
    print_color "   ✓ ملف .env.local موجود" "$YELLOW"
fi

# ============================================================================
# إنشاء دليل سريع
# ============================================================================

print_color "\n📖 إنشاء دليل سريع..." "$BLUE"

cat > QUICK_START_AR.md << 'GUIDE'
# 🚀 بدء سريع - Conscious Bridge Reloaded

## 🔧 الإعداد الأولي
