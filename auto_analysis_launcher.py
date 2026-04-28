#!/usr/bin/env python3
"""Windows executable launcher for Auto Analysis."""

from __future__ import annotations

import threading
import time
import urllib.request
import webbrowser

from app import app


HOST = "127.0.0.1"
PORT = 5057
URL = f"http://{HOST}:{PORT}/"


def open_browser_when_ready() -> None:
    for _ in range(60):
        try:
            with urllib.request.urlopen(URL, timeout=1):
                pass
            webbrowser.open(URL)
            return
        except Exception:
            time.sleep(1)


def main() -> None:
    print("Auto Analysis 서버를 시작합니다.")
    print("브라우저가 자동으로 열립니다.")
    print("이 창을 닫으면 Auto Analysis 서버도 종료됩니다.")
    threading.Thread(target=open_browser_when_ready, daemon=True).start()
    app.run(host=HOST, port=PORT, debug=False)


if __name__ == "__main__":
    main()
