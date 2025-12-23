#!/bin/bash

# Setup script cho lần đầu tiên

echo "🏢 RESIDENT MANAGEMENT SYSTEM - SETUP"
echo "======================================"
echo ""

# 1. Tạo virtual environment
echo "📦 Bước 1: Tạo virtual environment..."
python3 -m venv env
echo "✅ Đã tạo virtual environment!"
echo ""

# 2. Activate
echo "🔧 Bước 2: Activate virtual environment..."
source env/bin/activate
echo "✅ Đã activate!"
echo ""

# 3. Cài đặt dependencies
echo "📥 Bước 3: Cài đặt dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Đã cài đặt dependencies!"
echo ""

# 4. Migrations
echo "📊 Bước 4: Tạo database..."
python manage.py makemigrations
python manage.py migrate
echo "✅ Database đã sẵn sàng!"
echo ""

# 5. Tạo superuser
echo "👤 Bước 5: Tạo tài khoản admin..."
echo ""
echo "Nhập thông tin admin:"
python manage.py createsuperuser
echo ""

# 6. Hoàn tất
echo "======================================"
echo "✅ SETUP HOÀN TẤT!"
echo "======================================"
echo ""
echo "📝 Để chạy server lần sau, dùng lệnh:"
echo "   ./run.sh"
echo ""
echo "   Hoặc:"
echo "   source env/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "🚀 Bạn có muốn chạy server ngay bây giờ? (y/n)"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "🚀 Đang khởi động server..."
    echo ""
    echo "📍 Truy cập: http://127.0.0.1:8000/"
    echo "🔐 Admin:    http://127.0.0.1:8000/admin/"
    echo ""
    python manage.py runserver
else
    echo ""
    echo "👋 Chạy './run.sh' khi muốn khởi động server!"
fi

