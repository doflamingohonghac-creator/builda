# 🎮 HongHac Builda - Game MOD Tool

Ultra-secure game modding tool for Android (root required).

## 📱 Requirements

- Android device with root access
- Termux or Pydroid3
- Python 3.8+

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pkg install python git
pip install kivy pillow requests cryptography
```

### Step 2: Clone & Run
```bash
git clone https://github.com/doflamingohonghac-creator/builda.git
cd builda
python secure_loader.py
```

The app will automatically:
- Download encrypted package from cloud
- Decrypt with multi-layer security
- Launch the application

## 🔐 Security Features

- ✅ **Double-layer encryption** - AES-128 CBC with 2 different keys
- ✅ **Device binding** - App only runs on registered devices
- ✅ **Anti-debug** - Detects debuggers and exits
- ✅ **Time validation** - Prevents time manipulation
- ✅ **Integrity check** - Detects file modification
- ✅ **Obfuscated keys** - Keys split into byte arrays

**Security Level: 9.5/10** 🔒

## 📋 How It Works

1. User runs `secure_loader.py`
2. Loader downloads encrypted app from GitHub Release
3. First decryption with primary key
4. Second decryption with device-specific key
5. Integrity check
6. Execute in RAM (no disk write)

## ⚠️ Important Notes

- **First run requires internet** to download encrypted package
- **Device-specific** - Cannot copy to other devices
- **Root required** for full game modding functionality
- **Firebase key required** - Get key from app

## 🎯 Features

### MOD Capabilities
- ✨ Zoom (10-350%)
- 🔄 Rotation (0-360°)
- 💫 Opacity control (0-100%)
- 📐 Position offset (X/Y)
- 🔃 Flip (horizontal/vertical)

### Security System
- 🔐 Firebase key validation
- ⏰ Time-based expiration (10 minutes)
- 🚫 Attempt limiting (5 tries max)
- 🔍 Anti-crack detection
- 📱 Device fingerprinting

## 📞 Support

Issues? Contact: [Your contact here]

## 📜 License

This project is for educational purposes only.

---
**Made with ❤️ by HongHac Team**
