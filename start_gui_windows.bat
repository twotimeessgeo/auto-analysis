@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

set "PORT=5057"
set "URL=http://127.0.0.1:%PORT%/"
set "VENV_DIR=.venv"
set "PYTHON_BIN=%VENV_DIR%\Scripts\python.exe"

powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $c = Get-NetTCPConnection -LocalPort %PORT% -State Listen -ErrorAction Stop; if ($c) { exit 0 } } catch { exit 1 }"
if not errorlevel 1 (
  echo Auto Analysis 서버가 이미 실행 중입니다. 브라우저를 엽니다.
  start "" "%URL%"
  exit /b 0
)

if not exist "%PYTHON_BIN%" (
  echo.
  echo [처음 실행 준비]
  echo Python 가상환경과 필요한 패키지를 설치합니다.
  echo 처음 한 번만 1-3분 정도 걸릴 수 있습니다. 이 창을 닫지 마세요.
  echo.

  where py >nul 2>nul
  if not errorlevel 1 (
    py -3 -m venv "%VENV_DIR%"
  ) else (
    python -m venv "%VENV_DIR%"
  )
  if errorlevel 1 goto python_error

  "%PYTHON_BIN%" -m pip install --upgrade pip
  if errorlevel 1 goto install_error

  "%PYTHON_BIN%" -m pip install -r requirements.txt
  if errorlevel 1 goto install_error
)

echo.
echo Auto Analysis 서버를 시작합니다.
echo 브라우저가 자동으로 열립니다.
echo 이 창을 닫으면 Auto Analysis 서버도 종료됩니다.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Job { Start-Sleep -Seconds 2; Start-Process '%URL%' } | Out-Null"
"%PYTHON_BIN%" app.py

echo.
echo 서버가 종료되었습니다.
pause
exit /b 0

:python_error
echo.
echo Python 3을 찾지 못했습니다.
echo https://www.python.org/downloads/ 에서 Python 3.11 이상을 설치한 뒤 다시 실행하세요.
echo 설치 화면에서 Add python.exe to PATH를 체크하면 가장 쉽습니다.
pause
exit /b 1

:install_error
echo.
echo 필요한 패키지 설치에 실패했습니다.
echo 인터넷 연결을 확인한 뒤 다시 실행하세요.
pause
exit /b 1
