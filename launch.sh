#!/bin/bash
export FLASK_APP=src/driver.py
export FLASK_DEBUG=1
python3 -m flask run
