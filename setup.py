#!/usr/bin/env python3
"""A short script to set See3D up on a new computer."""
from getpass import getpass

# Set a unique secret key for CSRF and other security things.
secret_key = getpass('secret key: ')
with open('secret_key.py', 'w') as file:
    file.write("key = '{}'".format(secret_key))

# Create the database.
from See3D import db
db.create_all()
