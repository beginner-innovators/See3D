from flask import render_template
from See3D import app

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/profile/')
@app.route('/profile/<username>/')
def profile(username=""):
    return render_template('profile.html',
                           title='Profile',
                           user=username)
