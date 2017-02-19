from flask import render_template
from See3D import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': "Billy"}    # fake user
    return render_template('index.html')
