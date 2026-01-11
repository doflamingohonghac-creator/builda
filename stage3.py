# Stage 3: Binary Loader
import hashlib
import base64
import requests
from cryptography.fernet import Fernet
from Crypto.Cipher import AES

def get_device_fingerprint():
    """Get actual device fingerprint on Android"""
    try:
        import subprocess
        result = subprocess.run(
            "su -c 'settings get secure android_id'",
            shell=True, capture_output=True, text=True, timeout=5
        )
        android_id = result.stdout.strip()
        if android_id and android_id != "null":
            return "default_device_honghac_2026"  # Use same as encryption
    except:
        pass
    return "default_device_honghac_2026"

def generate_keys(device_fp):
    """Generate decryption keys"""
    key1_raw = hashlib.sha256(device_fp.encode()).digest()
    key1 = base64.urlsafe_b64encode(key1_raw)
    key2 = hashlib.sha256((device_fp + "_salt_aes").encode()).digest()[:16]
    key3 = hashlib.md5((device_fp + "_salt_xor").encode()).hexdigest()
    return key1, key2, key3

def xor_decrypt(data, key):
    """XOR decryption"""
    key_bytes = key.encode() if isinstance(key, str) else key
    key_len = len(key_bytes)
    return bytes(data[i] ^ key_bytes[i % key_len] for i in range(len(data)))

def triple_decrypt(encrypted_data, key1, key2, key3):
    """Triple decryption: Fernet → AES → XOR"""
    # Step 1: Fernet decrypt
    cipher_fernet = Fernet(key1)
    data = cipher_fernet.decrypt(encrypted_data)
    
    # Step 2: AES decrypt
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    cipher_aes = AES.new(key2, AES.MODE_EAX, nonce=nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    
    # Step 3: XOR decrypt
    data = xor_decrypt(data, key3)
    
    return data

def load_binary(bin_url):
    """Load and decrypt .bin file from URL or local"""
    print(f"[Layer 4] Loading binary: {bin_url}")
    
    # Try URL first
    try:
        if bin_url.startswith('http'):
            r = requests.get(bin_url, timeout=15)
            encrypted_data = r.content
        else:
            # Local file
            with open(bin_url, 'rb') as f:
                encrypted_data = f.read()
    except Exception as e:
        print(f"[!] Failed to load binary: {e}")
        return None
    
    # Get device fingerprint and keys
    fp = get_device_fingerprint()
    key1, key2, key3 = generate_keys(fp)
    
    # Decrypt
    try:
        decrypted_code = triple_decrypt(encrypted_data, key1, key2, key3)
        print(f"[OK] Binary decrypted: {len(decrypted_code)} bytes")
        return decrypted_code.decode('utf-8')
    except Exception as e:
        print(f"[!] Decryption failed: {e}")
        print(f"[!] Device fingerprint mismatch or corrupted file!")
        return None

# Load source_code.py from .bin
print("[Layer 4] === Loading encrypted binaries ===")
SOURCE_BIN_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/source_code.bin"
# Fallback to local
SOURCE_BIN_LOCAL = "source_code.bin"

source_code = load_binary(SOURCE_BIN_LOCAL)  # Try local first

if not source_code:
    print("[!] Failed to load source_code.bin!")
    import sys
    sys.exit(1)

# Execute in Layer 5 (RAM)
print("[Layer 5] === Executing in RAM ===")
exec(source_code)
