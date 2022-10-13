#!/bin/bash
cd A_1
# Install deps
pip install -r requirements.txt
# create database
python create_database.py
# Run the app
python app.py & python cache_app.py && kill $!

cd ..