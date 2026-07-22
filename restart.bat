@echo off
echo.
echo  Restarting LearnPath AI...
echo.

cd /d "%~dp0"

taskkill /F /IM streamlit.exe 2>nul
timeout /t 1 /nobreak >nul

echo  Starting...
echo  Open http://localhost:8501
echo.

python -m streamlit run frontend\app.py --server.headless true
pause
