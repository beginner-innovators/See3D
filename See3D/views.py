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
def about():
    return flask.render_template('about.html', title="About")

@app.route('/gallery/')
def gallery():
    requests = Request.query.all()
    return flask.render_template('gallery.html', title="Gallery", requests=requests)

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
    requests = Request.query.filter_by(email=current_user.email).all()
    return flask.render_template('profile.html', title="Profile", requests=requests)

@app.route('/oauth2callback')
def oauth2callback():
    # Create Google's provided object for sending a login request.
    flow = client.flow_from_clientsecrets(
        '../client_secrets.json',
        scope='email profile',
        redirect_uri=flask.url_for('oauth2callback', _external=True),
    )

    # Redirect user to Google sign-in.
    if 'error' in flask.request.args:
        if flask.request.args.get('error') == 'access_denied':
            flask.flash("You denied access")
        else:
            flask.flash("Some kind of error encountered during authorization.")

        return flask.redirect(flask.url_for('index'))

    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)

    # Upon callback, obtain the user's credentials.
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)

        flask.session['credentials'] = credentials.to_json()

        user_info = json.loads(flask.session['credentials'])

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
    if 'credentials' in flask.session:
        credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
        credentials.revoke(httplib2.Http())

    logout_user()
    return flask.redirect('index')

@app.route('/del_request/<request_id>/')
@login_required
def del_request(request_id):
    request = Request.query.get(int(request_id))

    if request.email == current_user.email:
        db.session.delete(request)
        db.session.commit()

        return flask.redirect(flask.url_for('profile'))

    else:
        return flask.redirect(flask.url_for('index'))
