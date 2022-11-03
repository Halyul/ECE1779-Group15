#!/bin/bash
cd A_2
# Install deps
pip install -r requirements.txt
# create database
python3 create_database.py
# Run the app
python3 app.py & python3 cache_app.py && kill $!

cd ..