#!/bin/bash

# Thoát nếu có lỗi
set -e

echo "🚀 Chạy generate_bz2.py..."
python generate_bz2.py   # ❗ dùng python thay vì python3

echo "📁 Thêm file vào Git..."
git add .

read -p "📝 Nhập nội dung commit: " message
git commit -m "$message"

echo "☁️ Đẩy lên GitHub..."
git push origin main

echo "✅ Hoàn tất!"
