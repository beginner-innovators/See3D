#!/usr/bin/env python3
import sys
from See3D import app

if "--production" in sys.argv:
    app.run(host='127.0.0.1', port=5000, debug=False)
else:
    app.run(host='127.0.0.1', port=5000, debug=True)