#!/bin/bash
# Install deps
pip install -r requirements.txt
# create database
python create_database.py
# Run the app
python app.py & python cache_app.py && kill $!