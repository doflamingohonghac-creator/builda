#!/usr/bin/env python3
"""
Bootstrap Loader - Entry Point for Multi-Layer Security System

This is the only file user runs: python bootstrap.py

Security Layers:
- Layer 1: This file (basic loader)
- Layer 2: Base64 obfuscation (optional)
- Layer 3: Fernet encryption (stage3.py)
- Layer 4: Triple-encrypted .bin files
- Layer 5: RAM-only execution

Usage:
    python bootstrap.py
"""

import os
import sys
import time

# === CONFIGURATION ===
USE_GITHUB = False  # Set True to load from GitHub, False for local
GITHUB_STAGE3_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/stage3.py"
LOCAL_STAGE3 = "stage3.py"

# === SECURITY CHECKS ===
def anti_debug_check():
    """Detect if debugger is attached"""
    if sys.gettrace() is not None:
        print("[WARNING] Debugger detected! Exiting...")
        sys.exit(1)

def check_required_files():
    """Check if required .bin files exist"""
    required_files = ['source_code.bin']
    missing = []
    
    for f in required_files:
        if not os.path.exists(f):
            missing.append(f)
    
    if missing:
        print(f"[ERROR] Missing required files: {', '.join(missing)}")
        print("\nPlease run encrypt_to_bin.py first to create .bin files")
        sys.exit(1)

# === LAYER 1: BOOTSTRAP ===
def display_banner():
    """Display startup banner"""
    print("=" * 60)
    print("  [SECURE] HONGHAC BUILDA - SECURE LOADER")
    print("  Multi-Layer Security System Active")
    print("=" * 60)
    print()

def load_stage3():
    """Load Stage 3 loader"""
    print("[Layer 1] Bootstrap initialization...")
    
    # Anti-debug check
    anti_debug_check()
    
    # Check required files
    check_required_files()
    
    print("[Layer 2] Loading stage3 loader...")
    
    # Load stage3.py
    if USE_GITHUB:
        print(f"  → Fetching from GitHub...")
        try:
            import requests
            r = requests.get(GITHUB_STAGE3_URL, timeout=10)
            if r.status_code == 200:
                stage3_code = r.text
                print("  [OK] Downloaded from GitHub")
            else:
                print(f"  [ERROR] GitHub fetch failed (HTTP {r.status_code})")
                print("  -> Falling back to local file...")
                with open(LOCAL_STAGE3, 'r', encoding='utf-8') as f:
                    stage3_code = f.read()
        except Exception as e:
            print(f"  [ERROR] GitHub error: {e}")
            print("  -> Falling back to local file...")
            with open(LOCAL_STAGE3, 'r', encoding='utf-8') as f:
                stage3_code = f.read()
    else:
        print(f"  -> Loading local file: {LOCAL_STAGE3}")
        try:
            with open(LOCAL_STAGE3, 'r', encoding='utf-8') as f:
                stage3_code = f.read()
            print("  [OK] Stage3 loaded")
        except FileNotFoundError:
            print(f"  [ERROR] {LOCAL_STAGE3} not found!")
            print("\nPlease run encrypt_to_bin.py first")
            sys.exit(1)
    
    return stage3_code

def execute_in_secure_namespace(code):
    """Execute code in isolated namespace"""
    print("[Layer 3] Preparing secure execution environment...\n")
    
    # Create isolated namespace
    namespace = {
        '__name__': '__main__',
        '__file__': '<memory>',
        '__builtins__': __builtins__,
    }
    
    # Execute stage3 (which will load and execute .bin files)
    try:
        exec(code, namespace)
    except Exception as e:
        print(f"\n❌ Execution error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# === MAIN ENTRY POINT ===
def main():
    """Main bootstrap function"""
    # Display banner
    display_banner()
    
    # Track startup time
    start_time = time.time()
    
    try:
        # Load stage3 loader
        stage3_code = load_stage3()
        
        # Execute in secure namespace
        execute_in_secure_namespace(stage3_code)
        
        # Calculate load time
        load_time = time.time() - start_time
        print(f"\n[TIME] Total load time: {load_time:.2f}s")
        
    except KeyboardInterrupt:
        print("\n\n[WARNING] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Bootstrap error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
