from auto_scaler import webapp
from auto_scaler.config import auto_scaler_port

webapp.run('0.0.0.0', int(auto_scaler_port), debug=False)