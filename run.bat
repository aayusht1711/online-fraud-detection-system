@echo off
title Project Aegis - SafeSight AI Security Server
cd /d "%~dp0"

echo ========================================================
echo   PROJECT AEGIS: SOC & REAL-TIME BOT DEFENSE PLATFORM
echo ========================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [!] Virtual environment not found. Creating .venv...
    python -m venv .venv
    echo [*] Installing dependencies from requirements.txt...
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
)

echo [*] Starting Flask Server on http://127.0.0.1:5000 ...
echo [*] Press CTRL+C to stop the server at any time.
echo.

.\.venv\Scripts\python.exe src\app.py
pause
