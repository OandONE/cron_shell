"""CronShell - ترمینال مخفی برای هاست‌های بدون SSH"""

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
COMMAND_FILE = BASE_DIR / "command.sh"
LOG_DIR = BASE_DIR / "logs"

# ─── Default Config ───
DEFAULT_CONFIG = {
    "sleep": 0,              # فاصله بین چک کردن command.sh (ثانیه)
    "log_retention": 7,      # چند روز لاگ نگه داره
    "timeout": 30,           # حداکثر زمان اجرای هر دستور (ثانیه)
    "max_log_size": 1048576, # حداکثر حجم هر لاگ (۱ مگابایت)
    "whitelist": [],         # دستورات مجاز (خالی = همه مجاز)
    "blacklist": ["rm -rf /", "mkfs", "dd if="],  # دستورات ممنوع
}


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return DEFAULT_CONFIG


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def is_safe(cmd: str, config: dict) -> bool:
    """چک کن دستور امن هست یا نه"""
    if config.get("whitelist"):
        return cmd.strip() in config["whitelist"]
    
    for bad in config.get("blacklist", []):
        if bad in cmd:
            return False
    
    return True


def cleanup_logs(config: dict):
    """پاک کردن لاگ‌های قدیمی"""
    retention = config.get("log_retention", 7)
    cutoff = time.time() - (retention * 86400)
    
    LOG_DIR.mkdir(exist_ok=True)
    for log_file in LOG_DIR.glob("*.log"):
        if log_file.stat().st_mtime < cutoff:
            log_file.unlink()


def execute_command(cmd: str, config: dict) -> tuple:
    """اجرای دستور و برگردوندن خروجی"""
    timeout = config.get("timeout", 30)
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(BASE_DIR)
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"⏰ Timeout after {timeout}s"


def main():
    config = load_config()
    LOG_DIR.mkdir(exist_ok=True)
    
    while True:
        cleanup_logs(config)
        
        if COMMAND_FILE.exists() and COMMAND_FILE.stat().st_size > 0:
            cmd = COMMAND_FILE.read_text().strip()
            
            COMMAND_FILE.write_text("")
            
            if not cmd:
                time.sleep(config["sleep"])
                continue
            
            if not is_safe(cmd, config):
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                log_file = LOG_DIR / f"result_{timestamp}.log"
                log_file.write_text(f"❌ Blocked unsafe command: {cmd}\n")
                time.sleep(config["sleep"])
                continue
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = LOG_DIR / f"result_{timestamp}.log"
            
            returncode, stdout, stderr = execute_command(cmd, config)
            
            log_content = f"""📅 {timestamp}
📝 Command: {cmd}
📊 Exit Code: {returncode}

─── STDOUT ───
{stdout}

─── STDERR ───
{stderr}
"""
            log_file.write_text(log_content)
        
        time.sleep(config["sleep"])


if __name__ == "__main__":
    main()
