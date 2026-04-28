#!/bin/zsh
cd "$(dirname "$0")"

PORT=5057
URL="http://127.0.0.1:${PORT}/"
VENV_DIR=".venv"
PYTHON_BIN="${VENV_DIR}/bin/python"

if ! lsof -nP -iTCP:${PORT} -sTCP:LISTEN >/dev/null 2>&1; then
  if [ ! -x "${PYTHON_BIN}" ]; then
    echo "처음 실행 준비 중입니다. 창을 닫지 마세요."
    python3 -m venv "${VENV_DIR}" || exit 1
    "${PYTHON_BIN}" -m pip install --upgrade pip
    "${PYTHON_BIN}" -m pip install -r requirements.txt || exit 1
  fi

  nohup "${PYTHON_BIN}" app.py > gui_server.log 2>&1 < /dev/null &
  sleep 2
fi

open "$URL"
