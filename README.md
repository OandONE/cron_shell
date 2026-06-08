<p align="center">
  <img src="https://raw.githubusercontent.com/OandONE/CronShell/main/static/logo.png" width="120" alt="CronShell">
</p>

<h1 align="center">⚡ CronShell</h1>
<p align="center"><strong>Hidden Terminal for Shared Hosts — No SSH Required</strong></p>

<p align="center">
  <a href="https://github.com/OandONE/CronShell/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="License: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue" alt="Python 3.8-3.14"></a>
</p>

---

## 🤔 Why?

Shared hosting (cPanel) usually blocks SSH access.  
You can't run `pip`, `git`, or even `ls -la` on your own server.

**CronShell** gives you a real terminal — powered by cron jobs and WebSocket.

---

## ✨ Features

- ✅ **No SSH needed** — works entirely through cron
- ✅ **Real-time WebPanel** — WebSocket + modern terminal UI
- ✅ **Dark theme** — looks like a real Linux terminal
- ✅ **Command history** — Arrow Up/Down
- ✅ **Token authentication** — no one else can access your panel
- ✅ **Log archive** — every command output saved to `logs/`
- ✅ **Safe mode** — blacklist dangerous commands
- ✅ **Lightweight** — pure Python, no database

---

## 📦 Installation

### 1. Upload files to your host

Upload the entire `CronShell/` folder to your shared host (e.g., `/home/user/CronShell/`).

### 2. Install dependencies (if you can)

```bash
pip install fastapi uvicorn
```

If pip is blocked, download these manually:

· fastapi
· uvicorn

3. Set up cron job

Add this to your cPanel cron jobs (every minute):

```bash
* * * * * /home/user/CronShell/runner.sh
```

4. Set your token

Edit config.json:

```json
{
    "token": "your-strong-secret-token-here",
    "sleep": 0,
    "timeout": 30,
    "whitelist": [],
    "blacklist": ["rm -rf /", "mkfs", "dd if="]
}
```

5. Start the web panel

```bash
cd /home/user/CronShell
python webpanel.py
```

Open in browser:

```
http://your-server-ip:9999/?token=your-strong-secret-token-here
```

---

🖥️ Screenshot

https://raw.githubusercontent.com/OandONE/CronShell/main/screenshot.png

---

📁 Project Structure

```
CronShell/
├── cronshell.py           # Core engine (run by cron)
├── webpanel.py            # WebSocket web panel (optional)
├── config.json            # Configuration
├── command.sh             # Command file (cron reads this)
├── runner.sh              # Cron entry point
├── logs/                  # Command output logs
├── static/
│   ├── panel.html         # Terminal UI
│   └── vazir.woff         # Persian font
└── README.md
```

---

🚀 Usage

Method 1: Web Panel (Real-time)

Open the panel, type commands, see output instantly.

Method 2: Command File (Cron)

Write your command in command.sh.
Cron runs cronshell.py every minute, executes it, saves output to logs/.

```bash
echo "pip list" > command.sh
# Wait 1 minute...
cat logs/result_*.log
```

---

🔒 Security

· Token required — set in config.json
· Blacklist — block dangerous commands
· Whitelist — allow only specific commands
· No open ports needed (for cron mode)

⚠️ Only use on servers you own or have permission to access.

---

📄 License

MIT © Seyyed Mohamad Hosein Moosavi Raja (OandONE)

---

🤝 Contributing

Pull requests are welcome.
Fork it, improve it, use it responsibly.
