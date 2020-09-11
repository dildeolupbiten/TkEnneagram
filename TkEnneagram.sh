var=$(python Scripts/check_venv.py)
if [ $var == "False" ]; then
    python3 -m pip install virtualenv
fi
if [ ! -d ./venv ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    python Scripts
else
    source venv/bin/activate
    python Scripts
fi
