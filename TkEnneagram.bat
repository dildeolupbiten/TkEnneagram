@echo off
python Scripts/check_venv.py > out
set /p var= < out
del out
if %var%==False (
    python -m pip install virtualenv
)
if exist ./venv (
    cd venv/Scripts
    activate.bat
    cd ../..
    python Scripts
) else (
    python -m venv venv
    cd venv/Scripts
    activate.bat
    python -m pip install --upgrade pip setuptools wheel
    cd ../..
    python -m pip install -r requirements.txt
    python Scripts
)
