@echo off

cd /d "%~dp0"

pip install -r dist/requirements.txt

py Authentication.py
py 2Back.py

pause
