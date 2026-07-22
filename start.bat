@echo off
title LearnPath AI - Starting...
echo ========================================
echo    LearnPath AI - Starting Application
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo Python OK!

echo.
echo [2/2] Starting Streamlit...
echo.
echo ========================================
echo    Open http://localhost:8501
echo    Press Ctrl+C to stop
echo ========================================
echo.

python -m streamlit run frontend\app.py --server.headless true

pause
