# استفاده از تصویر پایه Python
FROM python:3.9-slim

# تنظیم متغیرهای محیطی برای جلوگیری از بافر شدن خروجی Python
ENV PYTHONUNBUFFERED 1

# تنظیم دایرکتوری کاری داخل کانتینر
WORKDIR /app

# کپی کردن فایل requirements.txt به دایرکتوری کاری داخل کانتینر
COPY requirements.txt /app/

# نصب وابستگی‌های پروژه
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن بقیه فایل‌ها به دایرکتوری کاری داخل کانتینر
COPY . /app/

# فرمانی برای اجرای Celery worker
CMD ["celery", "-A", "online_store_kian", "worker", "--loglevel=info"]
