#!/usr/bin/env python3
import sys
from See3D import app

if '--debug=True' in sys.argv:
    app.run(host='127.0.0.1', port=5000, debug=True)
else:
    print(' * Running on production. Use the flag "--debug=True" for debug mode.')
    app.run(host='127.0.0.1', port=5000, debug=False)