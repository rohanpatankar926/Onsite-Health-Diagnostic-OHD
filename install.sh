#!bin/bash
echo "Installing the dependencies"
pip install -r requirements.txt

echo "Dependencies Installed"
echo "Starting the flask backend"
python3 app.py
