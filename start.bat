echo off
color 0A
cls

:: Check if the script is run as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    cd /d %~dp0
    title SOT Wayfinder
    pip install pydivert requests netaddr bs4
    cls
    python main.py
    pause
) else (
    echo Not running as administrator. Please run the script as administrator.
    echo.
    pause
    exit
)