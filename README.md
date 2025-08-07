# 🧪 SOCKS5 Proxy Checker with GitHub Actions

This project automatically checks a list of SOCKS5 proxies every 30 minutes using **GitHub Actions** and performs the following tasks:

## ✅ Features

- 🔁 Runs every 30 minutes (cron)
- 🧪 Tests each proxy for:
  - ✅ Liveness (connectivity)
  - 📶 Ping (latency)
  - 🌐 Geo IP location & ISP
  - 🚀 Download speed (via file fetch)
  - 🚀 Upload speed (via file upload)
- 📄 Outputs results in:
  - `proxies_result.md` (Markdown table)
  - `proxies_result.html` (Stylish HTML)
- ❌ Automatically removes dead proxies and opens a **pull request**

## 📁 Files Included

| File | Description |
|------|-------------|
| `check_proxies.py` | Main script that tests proxies and saves reports |
| `auto_pr_dead_proxies.py` | Script that removes dead proxies and opens a PR |
| `.github/workflows/proxy_check.yml` | GitHub Action to automate the process |
| `proxies.yaml` | (Dynamic) Loaded SOCKS5 proxy list |
| `alive_proxies.yaml` | (Generated) List of alive proxies |
| `proxies_result.md` | Proxy test results in Markdown |
| `proxies_result.html` | Proxy test results in HTML |

## 🚀 Usage

1. **Push this repo to GitHub**
2. **Enable GitHub Actions**
3. **Ensure `gh` CLI is authenticated** (used for PR creation)
4. ✅ Done — Proxy tests + reports + cleanup will auto-run every 30 mins

---

Made with ❤️ by [ChatGPT Automation]
