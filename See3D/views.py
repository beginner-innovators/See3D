from See3D import app

from flask import render_template, flash
from flask_login import login_user, logout_user, current_user, login_required

from auth import AuthenticationException

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

### Authentication Views ###
@app.route('/authorize/<provider>')
def oauth2authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth2callback(provider):
    if not current_user.is_anonymouse():
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)

    try:
        user_info = oauth.callback()       # Returns a JSON list of information about user

    except AuthenticationException:
        flash("Login failed - the request seems to be intended for another app.")
        return redirect(url_for('index'))

    

    email = user_info['email']
