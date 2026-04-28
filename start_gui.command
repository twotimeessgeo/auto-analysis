#!/bin/zsh
cd "$(dirname "$0")"

PORT=5057
URL="http://127.0.0.1:${PORT}/"

if ! lsof -nP -iTCP:${PORT} -sTCP:LISTEN >/dev/null 2>&1; then
  nohup python3 app.py > gui_server.log 2>&1 < /dev/null &
  sleep 1
fi

open "$URL"
