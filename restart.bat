@echo off
title LearnPath AI - Restarting...
echo ========================================
echo    LearnPath AI - Restarting Application
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Stopping existing processes...
taskkill /F /IM streamlit.exe 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501 ^| findstr LISTENING 2^>nul') do (
    taskkill /F /PID %%a 2>nul
)
timeout /t 2 /nobreak >nul

echo [2/2] Starting fresh...
echo.
echo ========================================
echo    Open http://localhost:8501
echo    Press Ctrl+C to stop
echo ========================================
echo.

python -m streamlit run frontend\app.py --server.headless true

pause
