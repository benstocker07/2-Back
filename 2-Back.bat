@echo off
py -m pyarmor.cli gen Task_Setup.py
py -m pyarmor.cli gen 2-Back.py
python dist/Task_Setup.py
pause
