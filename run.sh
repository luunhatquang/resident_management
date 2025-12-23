#!/bin/bash

# Script chạy nhanh Resident Management System

echo "🏢 RESIDENT MANAGEMENT SYSTEM"
echo "=============================="

# Kiểm tra virtual environment
if [ ! -d "env" ]; then
    echo "⚠️  Chưa có virtual environment!"
    echo "📦 Đang tạo virtual environment..."
    python3 -m venv env
    echo "✅ Đã tạo xong!"
fi

# Activate virtual environment
echo "🔧 Đang activate virtual environment..."
source env/bin/activate

# Cài đặt dependencies nếu chưa có
if ! python -c "import django" &> /dev/null; then
    echo "📥 Đang cài đặt dependencies..."
    pip install -r requirements.txt
fi

# Chạy migrations nếu cần
echo "🔄 Kiểm tra migrations..."
python manage.py migrate --check &> /dev/null
if [ $? -ne 0 ]; then
    echo "📊 Đang chạy migrations..."
    python manage.py migrate
fi

# Chạy server
echo ""
echo "✅ Sẵn sàng!"
echo "🚀 Khởi động server..."
echo ""
echo "📍 Truy cập: http://127.0.0.1:8000/"
echo "🔐 Admin:    http://127.0.0.1:8000/admin/"
echo ""
echo "⏹  Nhấn Ctrl+C để dừng server"
echo ""

python manage.py runserver

