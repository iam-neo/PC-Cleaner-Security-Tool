@echo off
REM PC Cleaner & Security Tool - Run as Administrator
REM This batch file runs the application with administrator privileges

echo ========================================
echo  PC Cleaner ^& Security Tool
echo  Starting with Administrator privileges...
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Run the application
python pc_cleaner_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check logs\app.log for details
    pause
)
