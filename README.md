
# 🧪 Proxy Speedtest Automation

This project automatically tests a list of SOCKS5 proxies using Playwright by visiting a custom speedtest website, capturing screenshots, and outputting results in Markdown and HTML.

---

## 📦 Features

- Fetches proxies from GitHub-hosted YAML (Catsx.txt)
- Tests latency and browser performance via http://zeroftp.speedtestcustom.com/
- Captures screenshots
- Outputs:
  - `proxies_result.md` (for GitHub display)
  - `proxies_result.html` (dark mode, emojis, responsive)
- GitHub Actions integration
  - Auto-run every 3 hours
  - Uploads result files as artifacts

---

## 🛠 Setup Locally

```bash
pip install -r requirements.txt
playwright install
python run_speedtest.py
```

Screenshots saved in `screenshots/`. Results in `proxies_result.md` and `proxies_result.html`.

---

## 🚀 GitHub Actions

The action is defined in `.github/workflows/proxy_speedtest.yml`. It runs every 3 hours and uploads results as artifacts.

---

## 🔗 Proxy Source

We fetch live proxies from:

```
https://raw.githubusercontent.com/Mushfiqtaief/ConfigXCats/refs/heads/main/Catsx.txt
```

---

## 🤖 Output Preview

Example Markdown and HTML views include proxy name, IP, port, status, and screenshot of test.

---

## 📁 Folder Structure

```
proxy_speedtest/
├── run_speedtest.py
├── requirements.txt
├── proxies_result.md
├── proxies_result.html
├── screenshots/
├── .github/
│   └── workflows/
│       └── proxy_speedtest.yml
└── README.md
```
