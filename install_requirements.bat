@echo off
title Project Aegis - Dependency Installer
cd /d "%~dp0"

echo ========================================================
echo   PROJECT AEGIS: INSTALLING DEPENDENCIES
echo ========================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [*] Creating virtual environment (.venv)...
    python -m venv .venv
)

echo [*] Upgrading pip...
.\.venv\Scripts\python.exe -m pip install --upgrade pip

echo [*] Installing requirements from requirements.txt...
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo [OK] All dependencies installed successfully!
pause
