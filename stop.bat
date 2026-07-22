@echo off
title LearnPath AI - Stopping...
echo ========================================
echo    LearnPath AI - Stopping Application
echo ========================================
echo.

echo Killing Streamlit processes...
taskkill /F /IM streamlit.exe 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq streamlit*" 2>nul

echo.
echo Looking for Streamlit on port 8501...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501 ^| findstr LISTENING') do (
    echo Killing process %%a
    taskkill /F /PID %%a 2>nul
)

echo.
echo ========================================
echo    Application stopped!
echo ========================================
echo.
pause
