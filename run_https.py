#!/usr/bin/env python3
import ssl
import sys

from See3D import app

if len(sys.argv) < 3:
    print("Missing parameters: ./run_https.py [cert] [key]")
    sys.exit()

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(sys.argv[1], sys.argv[2])

app.run(host='127.0.0.1', port=5000, debug=True, ssl_context=context)
