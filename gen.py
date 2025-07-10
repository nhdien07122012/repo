import os
import tarfile
import hashlib
import bz2
import io
import json
from typing import Dict

DEB_FOLDER = "debs"
OUTPUT_FILE = "Packages.txt"
BZIP_FILE = "Packages.bz2"
DESCRIPTION_FOLDER = "descriptions"
ICON_PATH = "file:///var/jb/Library/IconRepo/tinhchinh.png"
BASE_URL = "https://nhdien07122012.github.io/repo"

def extract_control_info_from_deb(deb_path: str) -> Dict[str, str]:
    control_info = {}
    with open(deb_path, "rb") as f:
        ar_content = f.read()

    files = {}
    i = 8  # skip "!<arch>\n"
    while i < len(ar_content):
        name = ar_content[i:i+16].decode("utf-8").strip()
        size = int(ar_content[i+48:i+58].decode("utf-8").strip())
        data = ar_content[i+60:i+60+size]
        if name.endswith("/"):
            name = name[:-1]
        files[name] = data
        i += 60 + size
        if size % 2 != 0:
            i += 1

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

def create_depiction(control, short_dir):
    version = control.get("Version", "1.0")
    description = control.get("Description", "Không có mô tả")

    depiction_data = {
        "minVersion": "0.1",
        "class": "DepictionTabView",
        "tintColor": "#0080ff",
        "headerImage": f"{BASE_URL}/sileo.png",
        "tabs": [
            {
                "tabname": "Mô tả",
                "class": "DepictionStackView",
                "tintColor": "#0080ff",
                "views": [
                    {
                        "class": "DepictionStackView",
                        "backgroundColor": "#0080ff",
                        "views": [
                            {
                                "class": "DepictionMarkdownView",
                                "tintColor": "#ffffff",
                                "markdown": "<style>body { color: white; text-align: center; }</style><br><strong>Ủng hộ tôi qua Momo: 039.9962.032</strong><br>&nbsp;",
                                "useRawFormat": True,
                                "useSpacing": False
                            }
                        ]
                    },
                    {
                        "class": "DepictionStackView",
                        "views": [
                            {
                                "class": "DepictionTableButtonView",
                                "title": "Xem mô tả gói tại đây",
                                "action": f"{BASE_URL}/descriptions/{short_dir}/{short_dir}.html",
                                "openExternal": False
                            },
                            {
                                "class": "DepictionTableButtonView",
                                "title": "Theo dõi tôi trên Facebook",
                                "action": "https://www.facebook.com/nhdien07122012/",
                                "openExternal": True
                            },
                            {
                                "class": "DepictionTableButtonView",
                                "title": "Ủng hộ tôi qua Momo",
                                "action": {
                                    "class": "DepictionAlertView",
                                    "title": "Ủng hộ qua Momo",
                                    "text": "SĐT: 039.9962.032\nTên: Nguyễn Diễn",
                                    "cancelButton": "Đóng"
                                },
                                "openExternal": False
                            },
                            {
                                "class": "DepictionImageView",
                                "URL": f"{BASE_URL}/images/momo_qr.png",
                                "height": 250,
                                "width": 250,
                                "alignment": 1,
                                "cornerRadius": 12
                            }
                        ]
                    },
                    {
                        "class": "DepictionMarkdownView",
                        "useBottomMargin": False,
                        "markdown": description,
                        "useBoldText": True,
                        "title": "markdown-description"
                    },
                    {
                        "class": "DepictionSeparatorView"
                    },
                    {
                        "class": "DepictionAdmobView",
                        "adUnitID": "ca-app-pub-9689973964248496/5297402136",
                        "adAppID": "ca-app-pub-9689973964248496~1758091302"
                    },
                    {
                        "class": "DepictionAdmobView",
                        "adUnitID": "ca-app-pub-9689973964248496/5297402136",
                        "adSize": "LargeBanner",
                        "adAppID": "ca-app-pub-9689973964248496~1758091302"
                    },
                    {
                        "class": "DepictionSpacerView",
                        "spacing": 2
                    },
                    {
                        "class": "DepictionImageView",
                        "URL": f"{BASE_URL}/CydiaIcon1.png",
                        "height": 200,
                        "width": 200,
                        "alignment": 1,
                        "cornerRadius": 0
                    },
                    {
                        "class": "DepictionSpacerView",
                        "spacing": 4
                    },
                    {
                        "class": "DepictionSpacerView",
                        "spacing": 4
                    }
                ]
            },
            {
                "tabname": "Nhật ký thay đổi",
                "class": "DepictionStackView",
                "tintColor": "#0080ff",
                "views": [
                    {
                        "class": "DepictionMarkdownView",
                        "markdown": f"### Phiên bản {version} - {description}",
                        "useRawFormat": True
                    }
                ]
            },
            {
                "tabname": "Liên hệ",
                "class": "DepictionStackView",
                "tintColor": "#0080ff",
                "views": [
                    {
                        "class": "DepictionMarkdownView",
                        "markdown": "### Liên hệ với tôi qua các nền tảng bên dưới:",
                        "useRawFormat": True
                    },
                    {
                        "class": "DepictionTableButtonView",
                        "title": "Facebook cá nhân",
                        "action": "https://www.facebook.com/nhdien07122012/",
                        "openExternal": True
                    },
                    {
                        "class": "DepictionTableButtonView",
                        "title": "Twitter cá nhân",
                        "action": "https://x.com/nguyenhoaidien?s=21",
                        "openExternal": True
                    },
                    {
                        "class": "DepictionTableButtonView",
                        "title": "Telegram cá nhân",
                        "action": "https://t.me/diennguyenhoai",
                        "openExternal": True
                    },
                    {
                        "class": "DepictionTableButtonView",
                        "title": "Zalo cá nhân",
                        "action": "https://zalo.me/0399962032",
                        "openExternal": True
                    }
                ]
            }
        ]
    }

    output_dir = os.path.join(DESCRIPTION_FOLDER, short_dir)
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "depiction.json"), "w", encoding="utf-8") as f:
        json.dump(depiction_data, f, ensure_ascii=False, indent=2)

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

                pkg = control.get('Package', 'unknown')
                short_dir = os.path.splitext(filename)[0].split("_")[0].split(".")[-1]

                create_depiction(control, short_dir)

                out_file.write(f"Package: {pkg}\n")
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
                out_file.write(f"Depiction: {BASE_URL}/descriptions/{short_dir}/depiction.json\n")
                out_file.write(f"SileoDepiction: {BASE_URL}/descriptions/{short_dir}/depiction.json\n")
                out_file.write(f"Name: {control.get('Name', '')}\n")
                out_file.write(f"Author: {control.get('Author', '')}\n")
                out_file.write(f"Sponsor: {control.get('Sponsor', '')}\n")
                out_file.write(f"Icon: {ICON_PATH}\n")
                out_file.write("\n")

    print("✅ Đã tạo file Packages.txt và depiction.json cho mỗi tweak")

def compress_bz2():
    with open(OUTPUT_FILE, "rb") as f_in:
        data = f_in.read()
    with bz2.open(BZIP_FILE, "wb") as f_out:
        f_out.write(data)
    print("🗜️ Đã tạo file Packages.bz2")

if __name__ == "__main__":
    generate_packages()
    compress_bz2()
