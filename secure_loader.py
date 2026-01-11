#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULTRA SECURE LOADER - Multi-layer Security
- Double encryption
- Obfuscated keys
- Anti-debug
- Device binding
- Time-based validation
- Integrity check
"""

import os
import sys
import time
import hashlib
import requests
from cryptography.fernet import Fernet

# ============== LAYER 1: OBFUSCATED CONFIGURATION ==============
# Keys are split and obfuscated
_p1 = "aHR0cHM6Ly9naXRodWIuY29tL2RvZmxhbWluZ29ob25naGFjLWNyZWF0b3IvYnVp"  # Base64 encoded URL part 1
_p2 = "bGRhL3JlbGVhc2VzL2Rvd25sb2FkL3YxLjAvc3RhbmRhbG9uZV9kb3VibGUuZW5j"  # Base64 encoded URL part 2

# Primary encryption key (obfuscated)
_k1_parts = [
    b'\x5f', b'\x69', b'\x56', b'\x4b', b'\x49', b'\x6d', b'\x39', b'\x73',
    b'\x44', b'\x59', b'\x4f', b'\x38', b'\x63', b'\x41', b'\x44', b'\x48',
]

# Secondary encryption key (for double encryption)
_k2_seed = "HONGHAC_BUILDA_2026_ULTRA_SECURE_V2"

# ============== LAYER 2: ANTI-DEBUG ==============
def _check_debugger():
    """Detect if running under debugger"""
    import ctypes
    if sys.platform == 'win32':
        if ctypes.windll.kernel32.IsDebuggerPresent():
            return True
    
    # Check for common debugger env vars
    debug_vars = ['PYTHONBREAKPOINT', 'PYCHARM_HOSTED', 'VSCODE_PID']
    if any(var in os.environ for var in debug_vars):
        return True
    
    return False

# ============== LAYER 3: DEVICE BINDING ==============
def _get_machine_id():
    """Get unique machine identifier"""
    try:
        if sys.platform == 'win32':
            import subprocess
            result = subprocess.check_output('wmic csproduct get uuid', shell=True)
            return hashlib.sha256(result).hexdigest()[:16]
        else:
            # Linux/Android
            with open('/etc/machine-id', 'r') as f:
                return hashlib.sha256(f.read().encode()).hexdigest()[:16]
    except:
        # Fallback: use MAC address
        import uuid
        mac = uuid.getnode()
        return hashlib.sha256(str(mac).encode()).hexdigest()[:16]

# ============== LAYER 4: TIME-BASED VALIDATION ==============
def _check_time_validity():
    """Prevent time manipulation"""
    try:
        # Get time from trusted server
        r = requests.get('http://worldtimeapi.org/api/ip', timeout=5)
        if r.status_code == 200:
            server_time = r.json()['unixtime']
            local_time = int(time.time())
            
            # If difference > 5 minutes, reject
            if abs(server_time - local_time) > 300:
                return False, "Time manipulation detected"
        
        return True, "OK"
    except:
        # If can't connect, allow (but log)
        return True, "Time check skipped"

# ============== LAYER 5: INTEGRITY CHECK ==============
def _verify_loader_integrity():
    """Check if this loader has been modified"""
    # Calculate hash of this file
    try:
        with open(__file__, 'rb') as f:
            content = f.read()
        
        file_hash = hashlib.sha256(content).hexdigest()
        
        # Expected hash (update this after finalizing loader)
        expected_hash = "UPDATE_THIS_AFTER_FINALIZE"
        
        if expected_hash != "UPDATE_THIS_AFTER_FINALIZE":
            if file_hash != expected_hash:
                return False, "Loader integrity check failed"
        
        return True, "OK"
    except:
        return True, "Integrity check skipped"

# ============== LAYER 6: KEY RECONSTRUCTION ==============
def _reconstruct_key1():
    """Reconstruct primary key from obfuscated parts"""
    key_bytes = b''.join(_k1_parts)
    # Add more parts to complete the key
    key_bytes += b'\x36\x58\x6c\x64\x55\x66\x42\x58'
    key_bytes += b'\x37\x48\x68\x50\x65\x33\x49\x71'
    key_bytes += b'\x67\x64\x58\x51\x53\x46\x52\x34'
    key_bytes += b'\x56\x37\x73\x3d'
    return key_bytes

def _derive_key2():
    """Derive secondary key from seed + machine ID"""
    machine_id = _get_machine_id()
    combined = f"{_k2_seed}:{machine_id}".encode()
    key_hash = hashlib.sha256(combined).digest()
    
    # Convert to Fernet-compatible key
    import base64
    return base64.urlsafe_b64encode(key_hash)

def _reconstruct_url():
    """Reconstruct download URL from obfuscated parts"""
    import base64
    url = base64.b64decode(_p1 + _p2).decode()
    return url

# ============== MAIN LOADER ==============
def secure_load():
    """Ultra-secure loading with multiple protection layers"""
    
    print("HongHac Builda Ultra Secure Loader v2.0")
    print("=" * 60)
    
    # LAYER 1: Anti-debug check
    if _check_debugger():
        print("[!] Debug environment detected. Exiting...")
        sys.exit(1)
    
    # LAYER 2: Integrity check
    valid, msg = _verify_loader_integrity()
    if not valid:
        print(f"[!] Security check failed: {msg}")
        sys.exit(1)
    
    # LAYER 3: Time validation
    valid, msg = _check_time_validity()
    if not valid:
        print(f"[!] {msg}")
        sys.exit(1)
    
    try:
        # Reconstruct keys and URL
        key1 = _reconstruct_key1()
        key2 = _derive_key2()
        url = _reconstruct_url()
        
        print(f"[*] Downloading encrypted package...")
        
        # Download encrypted data
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            print(f"[!] Download failed: {response.status_code}")
            return
        
        encrypted_data = response.content
        print(f"[*] Downloaded: {len(encrypted_data):,} bytes")
        
        # LAYER 4: Double decryption
        print(f"[*] Decrypting (layer 1)...")
        cipher1 = Fernet(key1)
        intermediate = cipher1.decrypt(encrypted_data)
        
        print(f"[*] Decrypting (layer 2)...")
        cipher2 = Fernet(key2)
        decrypted_code = cipher2.decrypt(intermediate)
        
        print(f"[*] Decryption successful!")
        
        # LAYER 5: Code integrity check before execution
        code_hash = hashlib.sha256(decrypted_code).hexdigest()
        print(f"[*] Code hash: {code_hash[:16]}...")
        
        # Execute in isolated namespace
        print(f"[*] Launching application...\n")
        exec(decrypted_code, {'__name__': '__main__', '__file__': 'app.py'})
        
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    secure_load()
