#!/bin/bash

# Thoát nếu có lỗi
set -e

echo "🚀 Chạy generate_bz2.py..."
python generate_bz2.py   # ❗ dùng python thay vì python3

echo "📁 Thêm file vào Git..."
git add .

echo "📝 Commit thay đổi..."
git commit -m "update repo"

echo "☁️ Đẩy lên GitHub..."
git push origin main

echo "✅ Hoàn tất!"
