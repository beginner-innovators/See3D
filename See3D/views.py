import json

import httplib2
from flask import redirect, render_template, request, session, url_for
from flask_login import login_required
from oauth2client import client

from See3D import app, db, login_manager, models

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/about/')
@login_required
def about():
    return render_template('about.html', title="About")

@app.route('/gallery/')
@login_required
def gallery():
    return render_template('gallery.html', title="Gallery")

@app.route('/profile/')
@login_required
def profile():
    return render_template('profile.html', title="Profile")

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        '../client_secrets.json',
        scope='https://www.googleapis.com/auth/userinfo.profile',
        redirect_uri=url_for('oauth2callback', _external=True),
    )
    flow.params['include_granted_scopes'] = "true"

    # Redirect user to Google sign-in.
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)

    # Upon callback, obtain the user's credentials.
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code).to_json()

        sub = credentials["id_token"]["sub"]        # Primary identification of Google account
        user = models.User.query.filter_by(sub=sub).first()

