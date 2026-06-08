"""CronShell WebPanel - پنل تحت وب با WebSocket و احراز هویت"""

import asyncio
import json
import subprocess
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn


BASE_DIR = Path(__file__).parent
COMMAND_FILE = BASE_DIR / "command.sh"
LOG_DIR = BASE_DIR / "logs"
CONFIG_FILE = BASE_DIR / "config.json"

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="CronShell WebPanel")

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

active_connections: dict[str, list[WebSocket]] = {}  # token -> [websockets]


def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)


def verify_token(token: str | None) -> bool:
    if not token:
        return False
    config = load_config()
    return token == config.get("token", "")


async def execute_cmd(cmd: str, timeout: int = 30) -> dict:
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(BASE_DIR)
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout
        )
        return {
            "exit_code": proc.returncode,
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
        }
    except asyncio.TimeoutError:
        return {
            "exit_code": -1,
            "stdout": "",
            "stderr": f"⏰ Timeout after {timeout}s",
        }


async def broadcast(token: str, msg: dict):
    for ws in active_connections.get(token, []):
        try:
            await ws.send_json(msg)
        except:
            active_connections[token].remove(ws)


@app.get("/")
async def index(token: str = Query(None)):
    if not verify_token(token):
        raise HTTPException(status_code=403, detail="⛔ دسترسی غیرمجاز. توکن معتبر نیست.")
    
    html = (BASE_DIR / "static" / "panel.html").read_text(encoding="utf-8")
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token", "")
    
    if not verify_token(token):
        await websocket.close(code=4001, reason="Unauthorized")
        return
    
    await websocket.accept()
    
    if token not in active_connections:
        active_connections[token] = []
    active_connections[token].append(websocket)
    
    await websocket.send_json({"type": "auth", "msg": "✅ احراز هویت موفق"})
    
    try:
        while True:
            data = await websocket.receive_json()
            cmd = data.get("command", "").strip()
            
            if not cmd:
                await websocket.send_json({"type": "error", "msg": "دستور خالیه"})
                continue
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            await broadcast(token, {"type": "running", "cmd": cmd, "time": timestamp})
            
            config = load_config()
            timeout = config.get("timeout", 30)
            result = await execute_cmd(cmd, timeout)
            
            log_name = f"result_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
            LOG_DIR.mkdir(exist_ok=True)
            log_content = f"""📅 {timestamp}
📝 Command: {cmd}
📊 Exit Code: {result['exit_code']}

─── STDOUT ───
{result['stdout']}

─── STDERR ───
{result['stderr']}
"""
            (LOG_DIR / log_name).write_text(log_content, encoding="utf-8")
            
            await broadcast(token, {
                "type": "result",
                "cmd": cmd,
                "time": timestamp,
                "exit_code": result["exit_code"],
                "stdout": result["stdout"],
                "stderr": result["stderr"],
            })
    
    except WebSocketDisconnect:
        active_connections[token].remove(websocket)


if __name__ == "__main__":
    print("🚀 CronShell WebPanel starting on http://0.0.0.0:9999")
    uvicorn.run(app, host="0.0.0.0", port=9999)
