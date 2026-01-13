# -*- coding: utf-8 -*-
import os

HONGHAC_DIR = "/storage/emulated/0/honghac"
DOWNLOAD_DIR = "/storage/emulated/0/Download"
MOD_DIR = "/storage/emulated/0/mod"
BG_URL = "https://github.com/doflamingohonghac-creator/builda/blob/main/background.png?raw=true"
APP_URL = "https://raw.githubusercontent.com/doflamingohonghac-creator/builda/refs/heads/main/honghac.py"

def download(url, path):
    import requests
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
    except:
        pass

if __name__ == "__main__":
    os.makedirs(HONGHAC_DIR, exist_ok=True)
    os.makedirs(MOD_DIR, exist_ok=True)
    download(BG_URL, os.path.join(HONGHAC_DIR, "background.png"))
    download(APP_URL, os.path.join(DOWNLOAD_DIR, "honghac.py"))
    print("DONE SETUP")
