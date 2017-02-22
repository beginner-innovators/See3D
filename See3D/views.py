from flask import render_template
from See3D import app

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html', title="About")

@app.route('/gallery/')
def gallery():
    return render_template('gallery.html', title="Gallery")

@app.route('/profile/')
def profile():
    return render_template('profile.html', title="Profile")
