@echo off
echo.
echo  Stopping LearnPath AI...
echo.

taskkill /F /IM streamlit.exe 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501 ^| findstr LISTENING 2^>nul') do taskkill /F /PID %%a 2>nul

echo  Stopped.
echo.
pause
