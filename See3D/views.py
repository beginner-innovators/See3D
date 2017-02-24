import json

import httplib2
import flask
from flask_login import current_user, login_required, login_user, logout_user
from oauth2client import client

from . import app, db, login_manager
from .forms import SubmitForm
from .models import User, Request

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@app.route('/index/')
def index():
    return flask.render_template('index.html')

@app.route('/about/')
@login_required
def about():
    return flask.render_template('about.html', title="About")

@app.route('/gallery/')
def gallery():
    requests = Request.query.all()

    return flask.render_template('gallery.html', title="Gallery", requests=requests)

@app.route('/requests/<request_id>/')
def request(request_id):
    return "Request {}".format(request_id)

@app.route('/submit/', methods=['GET', 'POST'])
@login_required
def submit():
    form = SubmitForm()

    if form.validate_on_submit():
        new_request = Request(title=form.title.data,
                              description=form.description.data,
                              email=current_user.email)

        db.session.add(new_request)
        db.session.commit()

        return flask.redirect(flask.url_for('gallery'))

    return flask.render_template('submit.html', title="Submit Request", form=form)

@app.route('/profile/')
@login_required
def profile():
    return flask.render_template('profile.html', title="Profile")

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        '../client_secrets.json',
        scope='email profile',
        redirect_uri=flask.url_for('oauth2callback', _external=True),
    )

    # Redirect user to Google sign-in.
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)

    # Upon callback, obtain the user's credentials.
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)

        user_info = json.loads(credentials.to_json())

        sub = user_info["id_token"]["sub"]        # Primary identification of Google account
        user = User.query.filter_by(sub=sub).first()

        # Add user to database if not already there.
        if not user:
            email = user_info["id_token"]["email"]
            user = User(email=email, creator=False, sub=sub)

            db.session.add(user)
            db.session.commit()

        login_user(user, remember=True)
        return flask.redirect(flask.url_for('index'))

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return flask.redirect('index')
