
import requests
import yaml
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from prettytable import PrettyTable

URL = "https://raw.githubusercontent.com/Mushfiqtaief/ConfigXCats/refs/heads/main/Catsx.txt"
SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

print("📥 Fetching proxy config from GitHub...")
response = requests.get(URL)
data = yaml.safe_load(response.text)

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for proxy in data['proxies']:
        name = proxy['name'][:30]
        ip = proxy['server']
        port = proxy['port']
        proxy_addr = f"socks5://{ip}:{port}"

        print(f"🚀 Testing {name} ({proxy_addr})")

        try:
            context = browser.new_context(proxy={"server": proxy_addr})
            page = context.new_page()
            page.goto("http://zeroftp.speedtestcustom.com/", timeout=30000)
            page.wait_for_timeout(20000)
            screenshot_path = SCREENSHOT_DIR / f"{name}.png"
            page.screenshot(path=str(screenshot_path))
            print(f"✅ Success: {screenshot_path}")
            results.append({"name": name, "ip": ip, "port": port, "status": "✅ Live", "screenshot": screenshot_path.name})
            context.close()
        except Exception as e:
            print(f"❌ Failed: {e}")
            results.append({"name": name, "ip": ip, "port": port, "status": "❌ Dead", "screenshot": None})

    browser.close()

# Markdown Output
table_md = "| Name | IP | Port | Status | Screenshot |\n|------|----|------|--------|------------|\n"
for r in results:
    shot = f"![{r['name']}](screenshots/{r['screenshot']})" if r['screenshot'] else "-"
    table_md += f"| {r['name']} | {r['ip']} | {r['port']} | {r['status']} | {shot} |\n"
with open("proxies_result.md", "w") as f:
    f.write(table_md)

# HTML Output
html = f"""
<html>
<head>
  <title>Proxy Results</title>
  <style>
    body {{ font-family: sans-serif; background: #111; color: #eee; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border: 1px solid #444; padding: 10px; }}
    th {{ background-color: #222; }}
    img {{ width: 320px; }}
  </style>
</head>
<body>
<h1>🧪 Proxy Test Results</h1>
<table>
  <tr><th>Name</th><th>IP</th><th>Port</th><th>Status</th><th>Screenshot</th></tr>
"""
for r in results:
    img = f'<img src="screenshots/{r["screenshot"]}">' if r['screenshot'] else '-'
    html += f"  <tr><td>{r['name']}</td><td>{r['ip']}</td><td>{r['port']}</td><td>{r['status']}</td><td>{img}</td></tr>\n"
html += "</table></body></html>"

with open("proxies_result.html", "w") as f:
    f.write(html)
