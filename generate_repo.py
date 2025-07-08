import os
import subprocess
import bz2

DEB_FOLDER = "debs"
OUTPUT_FILE = "Packages"
BZIP_FILE = "Packages.bz2"

def get_control_info(deb_path):
    control_data = {}
    try:
        # Giải nén control.tar.gz từ file .deb
        output = subprocess.check_output(["7z", "x", "-so", deb_path, "control.tar.gz"], stderr=subprocess.DEVNULL)
        with open("temp_control.tar.gz", "wb") as f:
            f.write(output)

        # Giải nén control file từ control.tar.gz
        subprocess.run(["7z", "x", "temp_control.tar.gz", "-aoa", "-o."], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Đọc file control
        with open("control", "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if ": " in line:
                    key, val = line.strip().split(": ", 1)
                    control_data[key] = val

        # Xoá file tạm
        os.remove("control")
        os.remove("temp_control.tar.gz")
    except Exception as e:
        print(f"⚠️ Không đọc được control info từ {deb_path}: {e}")
    return control_data

def generate_packages():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:
        for filename in os.listdir(DEB_FOLDER):
            if filename.endswith(".deb"):
                deb_path = os.path.join(DEB_FOLDER, filename)
                size = os.path.getsize(deb_path)
                control_info = get_control_info(deb_path)

                out_file.write(f"Filename: debs/{filename}\n")
                out_file.write(f"Size: {size}\n")
                for key in ["Package", "Version", "Architecture", "Maintainer", "Description", "Author", "Section"]:
                    if key in control_info:
                        out_file.write(f"{key}: {control_info[key]}\n")
                out_file.write("\n")
    print("✅ Đã tạo file Packages")

def compress_bz2():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "rb") as f_in:
            data = f_in.read()
        with bz2.open(BZIP_FILE, "wb") as f_out:
            f_out.write(data)
        print("🗜️ Đã tạo file Packages.bz2")

if __name__ == "__main__":
    generate_packages()
    compress_bz2()
