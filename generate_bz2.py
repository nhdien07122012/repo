import bz2

INPUT_FILE = "Packages"
OUTPUT_FILE = "Packages.bz2"

def compress_bz2():
    try:
        with open(INPUT_FILE, "rb") as f_in:
            data = f_in.read()
        with bz2.open(OUTPUT_FILE, "wb") as f_out:
            f_out.write(data)
        print("🗜️ Đã tạo file Packages.bz2 thành công.")
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file {INPUT_FILE}.")
    except Exception as e:
        print(f"⚠️ Lỗi khi nén file: {e}")

if __name__ == "__main__":
    compress_bz2()
