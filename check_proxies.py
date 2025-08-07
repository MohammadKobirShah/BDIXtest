# check_proxies.py
import yaml
import socks
import socket
import requests
import time
import json
import os
from tabulate import tabulate
from rich.console import Console
from rich.table import Table

GEO_API = "http://ip-api.com/json/"
TEST_DOWNLOAD_URL = "http://ipv4.download.thinkbroadband.com/10MB.zip"
TEST_UPLOAD_URL = "https://httpbin.org/post"
TIMEOUT = 10

console = Console()

def load_proxies(path="proxies.yaml"):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('proxies', [])

def test_proxy(proxy):
    ip = proxy['server']
    port = proxy['port']
    username = proxy.get('username')
    password = proxy.get('password')

    try:
        socks.set_default_proxy(socks.SOCKS5, ip, port, username, password)
        socket.socket = socks.socksocket
        start = time.time()
        s = socket.create_connection(("google.com", 80), timeout=TIMEOUT)
        ping = round((time.time() - start) * 1000)
        s.close()

        r = requests.get(GEO_API + ip, timeout=TIMEOUT)
        geo = r.json()
        location = f"{geo.get('country')}, {geo.get('city')}"
        isp = geo.get('isp')

        start = time.time()
        r = requests.get(TEST_DOWNLOAD_URL, timeout=TIMEOUT, stream=True)
        total = 0
        for chunk in r.iter_content(1024 * 100):
            total += len(chunk)
            if total > 1024 * 1024:  # 1MB
                break
        download_speed = round((total / 1024) / (time.time() - start), 2)  # KB/s

        start = time.time()
        files = {'file': ('test.txt', os.urandom(1024 * 100))}  # 100KB
        r = requests.post(TEST_UPLOAD_URL, files=files, timeout=TIMEOUT)
        upload_speed = round(100 / (time.time() - start), 2)  # KB/s

        return True, ping, location, isp, download_speed, upload_speed

    except Exception as e:
        return False, None, None, None, None, None

def main():
    proxies = load_proxies()
    results = []

    table = Table(title="🧪 Proxy Check Results", show_lines=True)
    table.add_column("Name")
    table.add_column("Ping (ms)")
    table.add_column("Location")
    table.add_column("ISP")
    table.add_column("⬇️ Download (KB/s)")
    table.add_column("⬆️ Upload (KB/s)")
    table.add_column("Status")

    alive_proxies = []

    for p in proxies:
        console.print(f"[yellow]Checking {p['name']}...[/yellow]")
        alive, ping, location, isp, down, up = test_proxy(p)
        if alive:
            table.add_row(p['name'], str(ping), location, isp, str(down), str(up), "✅ Alive")
            alive_proxies.append(p)
            results.append([p['name'], ping, location, isp, down, up, '✅ Alive'])
        else:
            table.add_row(p['name'], '-', '-', '-', '-', '-', "❌ Dead")
            results.append([p['name'], '-', '-', '-', '-', '-', '❌ Dead'])

    console.print(table)

    # Markdown output
    md = tabulate(results, headers=["Name", "Ping", "Location", "ISP", "Download KB/s", "Upload KB/s", "Status"], tablefmt="github")
    with open("proxies_result.md", "w") as f:
        f.write("# Proxy Check Results\n\n" + md)

    # HTML output
    html = tabulate(results, headers=["Name", "Ping", "Location", "ISP", "Download KB/s", "Upload KB/s", "Status"], tablefmt="html")
    with open("proxies_result.html", "w") as f:
        f.write("<html><body><h2>Proxy Check Results</h2>" + html + "</body></html>")

    # Save alive only for next script
    with open("alive_proxies.yaml", "w") as f:
        yaml.dump({"proxies": alive_proxies}, f)

if __name__ == '__main__':
    main()
