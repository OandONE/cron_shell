SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$SCRIPT_DIR/.cronshell.pid"

if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        exit 0
    fi
fi

nohup python3 "$SCRIPT_DIR/cronshell.py" > /dev/null 2>&1 &
echo $! > "$PID_FILE"
