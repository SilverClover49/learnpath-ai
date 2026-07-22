@echo off
title LearnPath AI
echo.
echo  Starting LearnPath AI...
echo  Open http://localhost:8501
echo  Press Ctrl+C to stop
echo.

cd /d "%~dp0"
python -m streamlit run frontend\app.py --server.headless true
pause
