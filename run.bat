@echo off
REM ============================================================
REM Script: run.bat
REM Purpose: Launch the SA JSSP GUI application
REM ============================================================

REM Change to project directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to your system PATH
    pause
    exit /b 1
)

echo Starting SA JSSP GUI Application...
echo.

REM Check if requirements are installed, install if needed
echo Checking dependencies...
python -c "import numpy; import matplotlib; import PIL" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirement.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies OK. Launching GUI...
echo.

REM Run the GUI
python gui/gui.py
if errorlevel 1 (
    echo [ERROR] Failed to launch GUI
    pause
    exit /b 1
)
