# 📱 HƯỚNG DẪN CÀI ĐẶT TRÊN TERMUX

## 📋 YÊU CẦU

- ✅ Android device (root)
- ✅ Termux app (Download: https://f-droid.org/en/packages/com.termux/)
- ✅ Kết nối internet

---

## 🚀 HƯỚNG DẪN CHI TIẾT

### BƯỚC 1: Cài đặt Termux

1. Tải Termux từ F-Droid (KHÔNG dùng Play Store)
2. Mở Termux
3. Cho phép storage access:
   ```bash
   termux-setup-storage
   ```
   → Click "Allow"

---

### BƯỚC 2: Update & Install Python

```bash
# Update packages
pkg update && pkg upgrade -y

# Install essentials
pkg install -y python git

# Install build dependencies
pkg install -y clang make libjpeg-turbo libpng

# Verify Python
python --version
# → Python 3.x.x
```

---

### BƯỚC 3: Install Dependencies

```bash
# Install pip packages
pip install --upgrade pip

# Install required packages (có thể mất 5-10 phút)
pip install kivy
pip install pillow
pip install requests
pip install cryptography

# Verify installations
python -c "import kivy; print('Kivy OK')"
python -c "import PIL; print('Pillow OK')"
python -c "import requests; print('Requests OK')"
python -c "from cryptography.fernet import Fernet; print('Crypto OK')"
```

**Lưu ý:** Nếu gặp lỗi khi cài Kivy:
```bash
pkg install -y python python-dev
pip install --upgrade cython
pip install kivy
```

---

### BƯỚC 4: Clone App

```bash
# Clone repository
git clone https://github.com/doflamingohonghac-creator/builda.git

# Vào folder
cd builda

# List files để verify
ls -la
# → Phải thấy: secure_loader.py, background.png, logo.png
```

---

### BƯỚC 5: Chạy App

```bash
# Chạy secure loader
python secure_loader.py
```

**Kết quả mong đợi:**
```
HongHac Builda Ultra Secure Loader v2.0
============================================================
[*] Downloading encrypted package...
[*] Downloaded: 158,284 bytes
[*] Decrypting (layer 1)...
[*] Decrypting (layer 2)...
[*] Decryption successful!
[*] Code hash: 3fa85f64b5a84006...
[*] Launching application...

[INFO] Kivy starting...
```

---

## ⚠️ TROUBLESHOOTING

### Lỗi: "No module named 'kivy'"
**Giải pháp:**
```bash
pip install --upgrade kivy
```

### Lỗi: "libjpeg not found"
**Giải pháp:**
```bash
pkg install libjpeg-turbo
pip uninstall pillow
pip install pillow --no-cache-dir
```

### Lỗi: "Download failed: 404"
**Nguyên nhân:** Chưa có internet hoặc URL sai

**Giải pháp:**
```bash
# Test internet
ping google.com

# Test GitHub access
curl -I https://github.com
```

### Lỗi: "Permission denied"
**Giải pháp:**
```bash
# Grant storage permission
termux-setup-storage

# If needed, run as root
su
cd /data/data/com.termux/files/home/builda
python secure_loader.py
```

### Lỗi: "Decryption failed"
**Nguyên nhân:** File bị corrupt hoặc key sai

**Giải pháp:**
```bash
# Xóa và clone lại
cd ~
rm -rf builda
git clone https://github.com/doflamingohonghac-creator/builda.git
cd builda
python secure_loader.py
```

---

## 🎯 SỬ DỤNG APP

### Lần đầu chạy:

1. App tải file encrypted từ GitHub
2. Click "LẤY KEY MỚI" → Browser mở
3. Copy key từ web
4. Paste vào app → "KÍCH HOẠT"
5. Key valid → Vào app

### Lần sau:

```bash
cd ~/builda
python secure_loader.py
```

App nhớ device ID → tự động load!

---

## 📂 CẤU TRÚC FOLDER

```
/data/data/com.termux/files/home/
  └── builda/
      ├── secure_loader.py    (Loader script)
      ├── background.png      (Background image)
      ├── logo.png            (Logo)
      └── README.md           (Documentation)
```

**Lưu ý:** File encrypted KHÔNG lưu local, chỉ download + decrypt trong RAM!

---

## 🔄 UPDATE APP

Khi có phiên bản mới:

```bash
cd ~/builda
git pull
python secure_loader.py
```

→ App tự động tải bản mới từ GitHub Release!

---

## 💡 TIPS & TRICKS

### 1. Tạo shortcut
```bash
# Tạo alias trong ~/.bashrc
echo "alias builda='cd ~/builda && python secure_loader.py'" >> ~/.bashrc
source ~/.bashrc

# Giờ chỉ cần gõ:
builda
```

### 2. Run in background
```bash
# Chạy background với nohup
nohup python secure_loader.py &

# Check process
ps aux | grep python
```

### 3. Auto-start khi mở Termux
```bash
# Thêm vào ~/.bashrc
echo "cd ~/builda && python secure_loader.py" >> ~/.bashrc
```

---

## 🛡️ BẢO MẬT

**Termux đã chạy:**
- ✅ Double encryption
- ✅ Device binding (từ /proc/sys/kernel/random/boot_id)
- ✅ Anti-debug (check debug env)
- ✅ Time validation
- ✅ Integrity check

**File encrypted chỉ tồn tại trong RAM, không lưu disk!**

---

## 📞 HỖ TRỢ

**Gặp vấn đề?**

1. Check log: `python secure_loader.py 2>&1 | tee error.log`
2. Gửi file `error.log` để được support
3. Hoặc tạo issue: https://github.com/doflamingohonghac-creator/builda/issues

---

## 📊 KIỂM TRA HỆ THỐNG

Chạy script này để check:

```bash
cat << 'EOF' > check_system.sh
#!/bin/bash
echo "=== System Check ==="
echo "Python: $(python --version 2>&1)"
echo "Git: $(git --version 2>&1)"
echo "Storage: $(df -h /data/data/com.termux/files/home | tail -1 | awk '{print $4}' ) free"
echo ""
echo "=== Python Packages ==="
python -c "import kivy; print('Kivy:', kivy.__version__)" 2>&1
python -c "import PIL; print('Pillow:', PIL.__version__)" 2>&1
python -c "import requests; print('Requests:', requests.__version__)" 2>&1
python -c "import cryptography; print('Cryptography:', cryptography.__version__)" 2>&1
echo ""
echo "=== Network ==="
ping -c 1 google.com > /dev/null && echo "Internet: OK" || echo "Internet: FAILED"
curl -I https://github.com > /dev/null 2>&1 && echo "GitHub: OK" || echo "GitHub: FAILED"
EOF

chmod +x check_system.sh
./check_system.sh
```

---

## ✅ CHECKLIST

Trước khi chạy app, check:

- [ ] Termux đã update
- [ ] Python installed
- [ ] Git installed
- [ ] pip packages installed
- [ ] Internet connected
- [ ] Storage permission granted
- [ ] Repository cloned
- [ ] Root access (nếu cần MOD game)

**Tất cả OK → `python secure_loader.py` → DONE!** 🎉
