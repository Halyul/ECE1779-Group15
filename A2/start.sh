#!/bin/bash
cd A_2
# Install deps
pip3 install -r requirements.txt
# Run the app
python3 manager_app.py & python3 auto_scaler_app.py & python3 app.py && jobs -p | xargs kill -9

cd ..
