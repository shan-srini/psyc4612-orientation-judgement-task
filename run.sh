#!/bin/bash

echo "PSYC4612 experiment generation"

echo "creating virtualenv using python3 if not exists"
python3 -m venv venv
echo "activating virtualenv"
. venv/bin/activate
echo "installing dependencies"
pip install -r requirements.txt
echo "generating stimuli"
python3 .

echo "finished"
