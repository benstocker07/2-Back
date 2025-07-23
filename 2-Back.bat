@echo off

py -m pyarmor.cli gen Task_Setup.py
py -m pyarmor.cli gen 2-Back.py
py -m pyarmor.cli gen MongoUpload.py

python dist/Task_Setup.py
python dist/MongoUpload.py

pause