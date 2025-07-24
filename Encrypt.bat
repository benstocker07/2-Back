@echo off

py -m pyarmor.cli gen Task_Setup.py
py -m pyarmor.cli gen 2-Back.py
py -m pyarmor.cli gen MongoUpload.py

REM python dist/Task_Setup.py
REM python dist/MongoUpload.py
REM pause