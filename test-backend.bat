@echo off
title LearnPath AI - Backend Test
echo ========================================
echo    LearnPath AI - Backend Test
echo ========================================
echo.

cd /d "%~dp0"

echo Running backend agent test...
echo This will take 30-60 seconds...
echo.

python -u backend\agent.py

echo.
echo ========================================
echo    Test Complete!
echo ========================================
echo.
pause
