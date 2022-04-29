#!/bin/bash

# This file will create a python virtual environment, activate and install all the APIs 
python3 -m venv ./forest_env # creates enviroment
echo "we have created the forest virtual enviroment"

. forest_env/bin/activate   # activates enviroment

pip install -r requirements.txt # installs APIs

deactivate