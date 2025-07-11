import os
import tarfile
import hashlib
import bz2
import io
import json
from typing import Dict
from datetime import datetime

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

def create_html_description(control, short_dir):
    name = control.get("Name", "Không có tên")
    author = control.get("Author", control.get("Maintainer", "Không rõ"))
    section = control.get("Section", "Tweaks")
    description = control.get("Description", "Không có mô tả")
    version = control.get("Version", "1.0.0")
    compatibility = control.get("Compatibility", "iOS 14.0 đến 17.0")
    today = datetime.now().strftime("%d/%m/%Y")

    html_content = f"""<!DOCTYPE html>
<html>
   <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1.0, user-scalable=0">
      <link rel="stylesheet" type="text/css" href="style.css">
      <style>a, .tint, .table-btn:after {{color: #5777B8}} .active {{color: #5777B8; border-bottom: 2px solid #5777B8;}}</style>
      <script src="../Bvn/Version.js"></script>
      <title>{name} - Diễn Nguyễn Repo</title>
   </head>
   <body>
      <div class="body">
      <div style="background-image: url({BASE_URL}/sileo.png)" class="banner_underlay"></div>
      <br><br>
      <div class="package package_head">
         <div class="package_info">
            <p class="text_cen">WELLCOME TO DIỄN NGUYỄN REPO</p>
         </div>
      </div>
      <div class="nav">
         <div class="nav_btn active tweak_info_btn" onclick="swap('.changelog','.tweak_info');">Chi tiết</div>
         <div class="nav_btn changelog_btn" onclick="swap('.tweak_info','.changelog');">Nhật ký thay đổi</div>
      </div>
      <div class="tweak_info">
         <p class="compatibility"></p>
         <br><br>
         <div class="md_view">
            <h2>Mô Tả & Giới thiệu</h2>
            <br>
            <h4>{name}</h4>
            <br>
            <p>
              {description}
            </p>
            <br><br><br>
            <h2>Hình ảnh</h2>
            <div class="scroll_view">
            <img class="imgcard" src="{BASE_URL}/images/{short_dir}/screenshot1.png" onerror="this.style.visibility='hidden';">
            <img class="imgcard" src="{BASE_URL}/images/{short_dir}/screenshot2.png" onerror="this.style.visibility='hidden';">
            <img class="imgcard" src="{BASE_URL}/images/{short_dir}/screenshot3.png" onerror="this.style.visibility='hidden';">
            </div>
         </div>
         <h2>Thông tin</h2>
         <br> 
         <div class="table">
            <div class="cell">
               <div class="title">Nhà phát triển</div>
               <div class="text">{author}</div>
               <br>
            </div>
            <div class="cell">
               <div class="title">Thể loại</div>
               <div class="text">{section}</div>
               <br>
            </div>
            <div class="cell">
               <div class="title">Ngày tải lên</div>
               <div class="text">{today}</div>
               <br>
            </div>
            <div class="cell">
               <div class="title">Khả năng tương thích</div>
               <div class="text">{compatibility}</div>
               <br><br>
            </div>
         </div>
      </div>
      <div class="changelog">
         <div class="changelog_entry">
            <h4>Phiên bản {version}</h4>
            <div class="md_view">
               <p>- Hỗ trợ Rootless</p>
            </div><br>
         </div>
      </div>
      <br><br>
      <img src="{BASE_URL}/CydiaIcon.png"  class="imageChange image_Center"/>
      <div class="caption center footer">
         <center>
            <div class="caption_center_footer" style="margin: 0 auto; width: 90%; display: flex; justify-content: center; gap: 20px;">
            <a href="tel:0399962032" style="display: flex; flex-direction: column; align-items: center; text-decoration: none;">
               <img src="{BASE_URL}/repo/icon-socials/phone.png" width="40" height="40" style="border-radius: 50%;">
               <span style="margin-top: 5px; font-size: 16px; color: white;">Phone</span>
            </a>
            <a href="https://www.facebook.com/nhdien07122012/" style="display: flex; flex-direction: column; align-items: center; text-decoration: none;">
               <img src="{BASE_URL}/repo/icon-socials/fb.png" width="40" height="40" style="border-radius: 50%;">
               <span style="margin-top: 5px; font-size: 16px; color: white;">Facebook</span>
            </a>
            <a href="https://x.com/nguyenhoaidien?s=21" style="display: flex; flex-direction: column; align-items: center; text-decoration: none;">
               <img src="{BASE_URL}/repo/icon-socials/twitter.png" width="40" height="40" style="border-radius: 50%;">
               <span style="margin-top: 5px; font-size: 16px; color: white;">Twitter</span>
            </a>
         </div>
         </center>
      </div>
      <p class="text_center">Copyright © {datetime.now().year} By Diễn Nguyễn</p>
   </body>
   <script>compatible("14.0","16.7.11","{compatibility}"); externalize()</script>
</html>"""

    output_dir = os.path.join(DESCRIPTION_FOLDER, short_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, f"{short_dir}.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

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

                original_pkg = control.get("Package", "unknown").lower()
                custom_pkg = f"{original_pkg}"
                short_dir = os.path.splitext(filename)[0].split("_")[0].split(".")[-1]

                create_depiction(control, short_dir)
                create_html_description(control, short_dir)  # Tạo file HTML

                out_file.write(f"Package: {custom_pkg}\n")
                out_file.write(f"Architecture: {control.get('Architecture', 'iphoneos-arm64')}\n")
                out_file.write(f"Version: {control.get('Version', '1.0.0')}\n")
                out_file.write(f"Section: {control.get('Section', 'Tweaks')}\n")
                out_file.write(f"Maintainer: Diễn Nguyễn\n")
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

    print("✅ Đã tạo file Packages.txt, depiction.json và HTML cho mỗi tweak")

def compress_bz2():
    with open(OUTPUT_FILE, "rb") as f_in:
        data = f_in.read()
    with bz2.open(BZIP_FILE, "wb") as f_out:
        f_out.write(data)
    print("🗜️ Đã tạo file Packages.bz2")

if __name__ == "__main__":
    generate_packages()
    compress_bz2()