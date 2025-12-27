@echo off
REM Script chạy nhanh Resident Management System cho Windows

echo ========================================
echo 🏢 RESIDENT MANAGEMENT SYSTEM
echo ========================================
echo.

REM Kiểm tra virtual environment
if not exist "env\" (
    echo ⚠️  Chưa có virtual environment!
    echo 📦 Đang tạo virtual environment...
    python -m venv env
    echo ✅ Đã tạo xong!
)

REM Activate virtual environment
echo 🔧 Đang activate virtual environment...
call env\Scripts\activate.bat

REM Cài đặt dependencies
echo 📥 Kiểm tra dependencies...
pip show django >nul 2>&1
if errorlevel 1 (
    echo 📥 Đang cài đặt dependencies...
    pip install -r requirements.txt
)

REM Chạy migrations
echo 🔄 Kiểm tra migrations...
python manage.py migrate

REM Chạy server
echo.
echo ✅ Sẵn sàng!
echo 🚀 Khởi động server...
echo.
echo 📍 Truy cập: http://127.0.0.1:8000/
echo 🔐 Admin:    http://127.0.0.1:8000/admin/
echo.
echo ⏹  Nhấn Ctrl+C để dừng server
echo.

python manage.py runserver
