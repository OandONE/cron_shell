"""CronShell WebPanel - Flask + WebSocket for cPanel compatibility"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from threading import Lock

from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit, disconnect

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
LOG_DIR = BASE_DIR / "logs"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24).hex()
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

connected_clients: dict[str, list[str]] = {}  # token -> [sid]
clients_lock = Lock()

PANEL_HTML = (BASE_DIR / "static" / "panel.html").read_text(encoding="utf-8")


def load_config():
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def verify_token(token: str | None) -> bool:
    if not token:
        return False
    config = load_config()
    return token == config.get("token", "")


def execute_cmd(cmd: str, timeout: int = 30) -> dict:
    """Run a shell command and return result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(BASE_DIR)
        )
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Timeout after {timeout}s",
        }


@app.route("/")
def index():
    token = request.args.get("token", "")
    
    if not verify_token(token):
        return "<h1 style='color:red;text-align:center;padding:40px;'>⛔ Access Denied: Invalid or missing token</h1>", 403
    
    html = PANEL_HTML.replace("__TOKEN_PLACEHOLDER__", token)
    return render_template_string(html)


@socketio.on("connect")
def handle_connect():
    token = request.args.get("token", "")
    
    if not verify_token(token):
        disconnect()
        return
    
    with clients_lock:
        if token not in connected_clients:
            connected_clients[token] = []
        connected_clients[token].append(request.sid) # pyright: ignore[reportAttributeAccessIssue]
    
    emit("message", {"type": "auth", "msg": "✅ Authenticated"})


@socketio.on("disconnect")
def handle_disconnect():
    with clients_lock:
        for token, sids in connected_clients.items():
            if request.sid in sids: # pyright: ignore[reportAttributeAccessIssue]
                sids.remove(request.sid) # pyright: ignore[reportAttributeAccessIssue]
                if not sids:
                    del connected_clients[token]
                break


@socketio.on("command")
def handle_command(data: dict):
    token = request.args.get("token", "")
    
    if not verify_token(token):
        emit("message", {"type": "error", "msg": "Unauthorized"})
        return
    
    cmd = data.get("command", "").strip()
    if not cmd:
        emit("message", {"type": "error", "msg": "Empty command"})
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    emit("message", {
        "type": "running",
        "cmd": cmd,
        "time": timestamp
    }, broadcast=True)
    
    config = load_config()
    timeout = config.get("timeout", 30)
    result = execute_cmd(cmd, timeout)
    
    LOG_DIR.mkdir(exist_ok=True)
    log_name = f"result_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    log_content = f"""[{timestamp}]
Command: {cmd}
Exit Code: {result['exit_code']}

--- STDOUT ---
{result['stdout']}

--- STDERR ---
{result['stderr']}
"""
    (LOG_DIR / log_name).write_text(log_content, encoding="utf-8")
    
    emit("message", {
        "type": "result",
        "cmd": cmd,
        "time": timestamp,
        "exit_code": result["exit_code"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
    }, broadcast=True)


if __name__ == "__main__":
    print("🚀 CronShell WebPanel (Flask) starting on http://0.0.0.0:9999")
    socketio.run(app, host="0.0.0.0", port=9999, allow_unsafe_werkzeug=True)

