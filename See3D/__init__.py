from flask import Flask

app = Flask(__name__)
from See3D import views       # Placed at end to avoid circular references
