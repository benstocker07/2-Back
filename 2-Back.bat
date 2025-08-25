@echo off

cd /d "%~dp0"

py dist/Task_Setup.py
py dist/Upload.py

pause
