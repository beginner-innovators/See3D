#!/usr/bin/env python3
import argparse
import ssl

from See3D import app

parser = argparse.ArgumentParser(description='Start up the server for See3D.')

parser.add_argument('-d', '--debug', action='store_true',
                    help='run the server in debug mode.')
parser.add_argument('--host', default='127.0.0.1',
                    help='specify the ip address on which to run the server')
parser.add_argument('--port', type=int, default=5000,
                    help='specify the port on which to run the server')
parser.add_argument('--https', nargs=2, metavar=('CERT', 'KEY'),
                    help='run the server on https given the paths to the SSL certificate and key')

args = parser.parse_args()

if args.https:
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(args.https[0], args.https[1])

    app.run(host=args.host, port=args.port, debug=args.debug, ssl_context=context)

else:
    app.run(host=args.host, port=args.port, debug=args.debug)
