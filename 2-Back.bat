@echo off
py -m pyarmor.cli gen Task_Setup.py
python dist/Task_Setup.py
pause
