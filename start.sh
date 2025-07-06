#!/bin/bash

source venv/bin/activate

export PYTHONPATH=$(pwd)
python3 ./src/main.py

deactivate