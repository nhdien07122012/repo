import os
import tarfile
import tempfile
import hashlib
import bz2
import io
from typing import Dict

DEB_FOLDER = "debs"
OUTPUT_FILE = "Packages.txt"
BZIP_FILE = "Packages.bz2"

def extract_control_info_from_deb(deb_path: str) -> Dict[str, str]:
    control_info = {}
    with open(deb_path, "rb") as f:
        ar_content = f.read()

    # Parse .deb = ar archive
    files = {}
    i = 8  # skip header "!<arch>\n"
    while i < len(ar_content):
        name = ar_content[i:i+16].decode("utf-8").strip()
        size = int(ar_content[i+48:i+58].decode("utf-8").strip())
        data = ar_content[i+60:i+60+size]
        if name.endswith("/"):
            name = name[:-1]
        files[name] = data
        i += 60 + size
        if size % 2 != 0:
            i += 1  # skip padding byte

    # Find control.tar.*
    for control_file in ["control.tar.gz", "control.tar.xz", "control.tar.bz2"]:
        if control_file in files:
            fileobj = io.BytesIO(files[control_file])
            with tarfile.open(fileobj=fileobj, mode="r:*") as tar:
                for member in tar.getmembers():
                    if os.path.basename(member.name) == "control":
                        control = tar.extractfile(member).read().decode("utf-8")
                        for line in control.strip().split("\n"):
                            if ": " in line:
                                key, val = line.split(": ", 1)
                                control_info[key.strip()] = val.strip()
                        return control_info
            break
    raise ValueError("Không tìm thấy file control trong .deb")


def generate_hashes(filepath):
    hashes = {
        "MD5sum": hashlib.md5(),
        "SHA1": hashlib.sha1(),
        "SHA256": hashlib.sha256(),
        "SHA512": hashlib.sha512()
    }
    with open(filepath, "rb") as f:
        content = f.read()
        for h in hashes.values():
            h.update(content)
    return {k: h.hexdigest() for k, h in hashes.items()}

def generate_packages():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_file:
        for filename in os.listdir(DEB_FOLDER):
            if filename.endswith(".deb"):
                deb_path = os.path.join(DEB_FOLDER, filename)
                size = os.path.getsize(deb_path)
                control = extract_control_info_from_deb(deb_path)
                hashes = generate_hashes(deb_path)

                out_file.write(f"Package: {control.get('Package', 'unknown')}\n")
                out_file.write(f"Architecture: {control.get('Architecture', 'iphoneos-arm64')}\n")
                out_file.write(f"Version: {control.get('Version', '1.0.0')}\n")
                out_file.write(f"Section: {control.get('Section', 'Tweaks')}\n")
                out_file.write(f"Maintainer: {control.get('Maintainer', 'Unknown')}\n")
                out_file.write(f"Installed-Size: {control.get('Installed-Size', '1024')}\n")
                if "Depends" in control:
                    out_file.write(f"Depends: {control['Depends']}\n")
                out_file.write(f"Filename: ./debs/{filename}\n")
                out_file.write(f"Size: {size}\n")
                out_file.write(f"MD5sum: {hashes['MD5sum']}\n")
                out_file.write(f"SHA1: {hashes['SHA1']}\n")
                out_file.write(f"SHA256: {hashes['SHA256']}\n")
                out_file.write(f"SHA512: {hashes['SHA512']}\n")
                out_file.write(f"Description: {control.get('Description', 'No description')}\n")
                out_file.write(f"Depiction: {control.get('Depiction', '')}\n")
                out_file.write(f"SileoDepiction: {control.get('SileoDepiction', '')}\n")
                out_file.write(f"Name: {control.get('Name', '')}\n")
                out_file.write(f"Author: {control.get('Author', '')}\n")
                out_file.write(f"Sponsor: {control.get('Sponsor', '')}\n")
                out_file.write(f"Icon: {control.get('Icon', '')}\n")
                out_file.write("\n")
    print("✅ Đã tạo file Packages")

def compress_bz2():
    with open(OUTPUT_FILE, "rb") as f_in:
        data = f_in.read()
    with bz2.open(BZIP_FILE, "wb") as f_out:
        f_out.write(data)
    print("🗜️ Đã tạo file Packages.bz2")

if __name__ == "__main__":
    generate_packages()
    #compress_bz2()
