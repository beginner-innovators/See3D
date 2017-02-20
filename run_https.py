#!/usr/bin/env python3
import ssl
from See3D import app

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('../stunnel.cert', '../stunnel.key')

app.run(host='127.0.0.1', port=5000, debug=True, ssl_context=context)
