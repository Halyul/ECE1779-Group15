#!/bin/bash
# Install deps
pip install -r requirements.txt
# Run the app
python app.py & python cache_app.py && kill $!