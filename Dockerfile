# Conscious Bridge Reloaded - Docker Image
FROM python:3.11-slim

# إعداد المتغيرات البيئية
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

# إنشاء دليل التطبيق
WORKDIR $APP_HOME

# تثبيت متطلبات النظام
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# نسخ المتطلبات
COPY requirements.txt .

# تثبيت حزم Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# إنشاء مجلدات البيانات
RUN mkdir -p data logs backups exports

# تعيين الصلاحيات
RUN chmod +x scripts/*.py scripts/*.sh

# المنفذ
EXPOSE 5000

# أمر التشغيل
CMD ["python", "-m", "api.server"]
