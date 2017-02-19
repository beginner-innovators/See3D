from flask import render_template
from See3D import app

requests = [{'user': 'Barbara', 'body': 'Toy Train'},
            {'user': 'Miguel', 'body': 'Globe'},
            {'user': 'Jennifer', 'body': 'Photograph'}]
test_user = {"username": "Billy", "requests": requests}

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/profile/')
@app.route('/profile/<username>/')
def profile(username=""):
    if username.lower() == test_user["username"].lower():
        user = test_user
    else:
        user = None

    return render_template('profile.html',
                           title="Profile",
                           user=user)

