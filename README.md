<p align="center">
  <img src="https://raw.githubusercontent.com/OandONE/cron_shell/main/static/logo.png" width="120" alt="cron_shell">
</p>

<h1 align="center">⚡ CronShell</h1>
<p align="center"><strong>Hidden Terminal for Shared Hosts — No SSH Required</strong></p>

<p align="center">
  <a href="https://github.com/OandONE/cron_shell/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="License: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue" alt="Python 3.8-3.14"></a>
</p>

---

## 🤔 Why CronShell?

Shared hosting (cPanel, DirectAdmin) usually blocks SSH access.  
You're locked out of your own server. Can't run `pip`, `git`, `composer`, or even `ls -la`.

**CronShell** gives you a real terminal — powered by cron jobs and WebSocket.  
No SSH. No open ports. No pain.

---

## ✨ Features

- 🔒 **No SSH needed** — works entirely through cron
- 🌐 **Real-time WebPanel** — WebSocket-powered terminal UI
- 🎨 **Dark theme** — looks exactly like a Linux terminal
- 📜 **Command history** — Arrow Up/Down
- 🔑 **Token authentication** — no one else can access
- 📁 **Log archive** — every command output saved to `logs/`
- 🛡️ **Safe mode** — blacklist/whitelist dangerous commands
- 🪶 **Lightweight** — pure Python, no database
- 📦 **cPanel compatible** — Flask + Socket.IO version included

---

## 📁 Project Structure

```
cron_shell/
├── README.md
├── README_FA.md
│
└── cron_shell/
    ├── cronshell.py              # 🔧 Core engine (run by cron)
    ├── webpanel.py               # 🌐 Flask + Socket.IO WebPanel
    ├── webpanel_fastapi.py       # ⚡ FastAPI + WebSocket WebPanel
    ├── runner.sh                 # 🏃 Cron entry point
    ├── config.json               # ⚙️ Configuration
    ├── crontab                   # 📅 Sample cron job
    └── static/
        ├── panel.html            # 🖥️ Terminal UI (Flask version)
        ├── panel_fastapi.html    # 🖥️ Terminal UI (FastAPI version)
        └── vazir.woff2           # 🇮🇷 Persian font
```

---

## 🐍 Python Files Explained

### 1. `cronshell.py` — Core Engine

The main script that cron runs every minute (via `runner.sh`).

**What it does:**
- Checks if `command.sh` has content
- If yes: executes the command, saves output to `logs/`, clears `command.sh`
- Supports whitelist/blacklist for safety
- Log rotation (auto-deletes old logs)

**Use this when:** you don't need the web panel. Just write commands in `command.sh`.

```bash
echo "ls -la /home" > command.sh
# Wait 1 minute...
cat logs/result_*.log
```

---

### 2. `webpanel.py` — Flask WebPanel

Web-based terminal with real-time output via **Flask + Socket.IO**.

**What it does:**
- Serves a terminal-style HTML page
- Connects via WebSocket (Socket.IO)
- Executes commands and shows output instantly
- Token-based authentication
- Saves all outputs to `logs/`

**Use this when:** you're on **cPanel/shared hosting** (where ASGI doesn't work).

**Start:**
```bash
pip install flask flask-socketio
python webpanel.py
# Open: http://your-server:9999/?token=YOUR_TOKEN
```

---

### 3. Set Execute Permission for runner.sh

The cron job needs execute permission to run `runner.sh` :

1. Open **File Manager** in cPanel
2. Navigate to `cron_shell/`
3. **Click once** on `runner.sh` (single click, not double)
4. Click **Permissions** in the top toolbar
5. Check **Execute** for **User** row:

```
User:  [✓] Read  [✓] Write  [✓] Execute
Group: [✓] Read  [ ] Write  [ ] Execute
World: [✓] Read  [ ] Write  [ ] Execute
```

6. Click **Change Permissions**

Done. The file can now be executed by cron.

---

### 4. `webpanel_fastapi.py` — FastAPI WebPanel

Same as Flask version, but built with **FastAPI + native WebSocket**.

**What it does:**
- Everything `webpanel.py` does
- Native async support (better performance)
- Cleaner WebSocket handling

**Use this when:** you're on a **VPS or dedicated server** (ASGI works fine).

**Start:**
```bash
pip install fastapi uvicorn
python webpanel_fastapi.py
# Open: http://your-server:9999/?token=YOUR_TOKEN
```

---

## 📦 Installation

### 1. Upload to your host

Upload the `cron_shell/` folder to your shared host or VPS.

### 2. Set up cron job

Copy the content of `crontab` file to your cPanel **Cron Jobs**:

```bash
* * * * * /home/youruser/cron_shell/runner.sh
```

### 3. Configure your token

Edit `config.json`:

```json
{
    "token": "your-strong-secret-token-here",
    "sleep": 0,
    "timeout": 30,
    "log_retention": 7,
    "whitelist": [],
    "blacklist": ["rm -rf /", "mkfs", "dd if="]
}
```

### 4. Start the web panel

```bash
cd /home/youruser/cron_shell

# For cPanel / shared hosting:
python webpanel.py

# For VPS:
python webpanel_fastapi.py
```

### 5. Open in browser

```
http://your-server-ip:9999/?token=your-strong-secret-token-here
```

---

## 🔒 Security

- **Token required** — set in `config.json`
- **Blacklist** — block dangerous commands
- **Whitelist** — allow only specific commands
- **No open ports** needed (for cron-only mode)

> ⚠️ Only use on servers you own or have explicit permission to access.

---

## 📄 License

MIT © [Seyyed Mohamad Hosein Moosavi Raja (OandONE)](https://github.com/OandONE)

---

## 🤝 Contributing

Pull requests are welcome.  
Found a bug? Open an issue.  
Want to add a feature? Fork it.
```

---
