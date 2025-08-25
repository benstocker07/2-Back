@echo off

cd /d "%~dp0"

pip install -r requirements.txt

py dist/Task_Setup.py
py dist/Upload.py

pause
