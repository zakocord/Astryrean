@echo off

python.exe -m pip install --upgrade pip

pip uninstall -r interact.txt
pip install -r requirements.txt
py gui.py
pause
