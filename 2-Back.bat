@echo off

cd /d "%~dp0"

pip install -r dist/requirements.txt

py dist/Task_Setup.py
py dist/Upload.py

pause
