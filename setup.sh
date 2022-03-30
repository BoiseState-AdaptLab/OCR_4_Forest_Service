#!/bin/bash
# This file will create a python virtual environment, activate and install all the APIs 
python -m venv ./venv # creates enviroment
. venv/bin/activate   # activates enviroment

pip install -r requirements.txt # installs APIs

deactivate