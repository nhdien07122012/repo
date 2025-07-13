#!/bin/bash

# Thư mục chứa các thư mục đã giải nén
INPUT_DIR="final"
# Thư mục chứa các file .deb được đóng gói lại
OUTPUT_DIR="output_debs"

# Tạo thư mục output nếu chưa có
mkdir -p "$OUTPUT_DIR"

echo "🔁 Đang build lại các file .deb từ thư mục $INPUT_DIR ..."

# Duyệt từng thư mục con trong final/
for dir in "$INPUT_DIR"/*; do
    if [ -d "$dir" ]; then
        pkg_name=$(basename "$dir")
        output_path="$OUTPUT_DIR/$pkg_name.deb"
        
        echo "📦 Đang build: $pkg_name → $output_path"
        dpkg-deb -b "$dir" "$output_path"

        # Kiểm tra lỗi
        if [ $? -eq 0 ]; then
            echo "✅ Thành công: $pkg_name"
        else
            echo "❌ Thất bại: $pkg_name"
        fi
    fi
done

echo "✅ Đã hoàn tất."