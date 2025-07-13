#!/bin/bash

# Kiểm tra đầu vào
if [ -z "$1" ]; then
  echo "❌ Vui lòng cung cấp đường dẫn đến file .deb"
  echo "Cách dùng: ./extract-deb.sh yourfile.deb"
  exit 1
fi

DEB_FILE="$1"
BASENAME=$(basename "$DEB_FILE" .deb)
EXTRACT_DIR="./$BASENAME"

# Tạo thư mục giải nén
mkdir -p "$EXTRACT_DIR/DEBIAN"

echo "📦 Đang giải nén: $DEB_FILE → $EXTRACT_DIR"

# Giải nén control (DEBIAN)
dpkg-deb -e "$DEB_FILE" "$EXTRACT_DIR/DEBIAN"
if [ $? -ne 0 ]; then
  echo "❌ Giải nén DEBIAN thất bại!"
  exit 1
fi

# Giải nén data (các file hệ thống như /Library,...)
dpkg-deb -x "$DEB_FILE" "$EXTRACT_DIR"
if [ $? -ne 0 ]; then
  echo "❌ Giải nén dữ liệu thất bại!"
  exit 1
fi

echo "✅ Đã giải nén thành công vào thư mục: $EXTRACT_DIR"
