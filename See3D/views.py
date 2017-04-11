from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from oauth2client import client, crypt

from . import app, db, login_manager
from .forms import SubmitForm
from .models import User, Request


@login_manager.user_loader
def load_user(user_id):
    """Return the id of a User object so that flask_login can find it in the database."""
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/index/')
def index():
    """Render a simple about page with options to login or signup."""
    return render_template('index.html')


@app.route('/oauth2callback', methods=['GET', 'POST'])
def oauth2callback():
    """Receive and validate Google's id token, then use the 'sub' field to store and log the user in to a session."""
    if request.method == 'POST':
        token = request.form.get('idtoken')

        # Use Google's process to verify the received id token.
        try:
            idinfo = client.verify_id_token(token, '151432626794-3svgnd49h2fjmngk1cuatmrmna5n05jl.apps.googleusercontent.com')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")

        except crypt.AppIdentityError:
            flash('The submitted login token is invalid.')
            return "login failed"

        user = User.query.filter_by(sub=idinfo['sub']).first()

        # Add user to database if not already there.
        if not user:
            user = User(sub=idinfo['sub'], is_creator=False, email=idinfo['email'], name=idinfo['name'])

            db.session.add(user)
            db.session.commit()

        login_user(user, remember=False)
        return user.email

    elif request.method == 'GET':
        return redirect(url_for('index'))


@app.route('/about/')
@login_required
def about():
    """Render a simple about page."""
    return render_template('about.html', title="Our Project")
        

@app.route('/gallery/')
@login_required
def gallery():
    """Render a scrollable gallery of all currently active requests."""
    if current_user.is_creator is True:
        return render_template('gallery.html', title="Gallery", requests=Request.query.all())

    else:
        return redirect(url_for('profile'))


@app.route('/submit/', methods=['GET', 'POST'])
@login_required
def submit():
    """Render and accept data from a form to submit a request."""
    form = SubmitForm()

    if form.validate_on_submit():
        new_request = Request(title=form.title.data,
                              description=form.description.data)

        current_user.requests.append(new_request)

        db.session.add(new_request)
        db.session.commit()

        return redirect(url_for('gallery'))

    return render_template('submit.html', title="Create Request", form=form)


@app.route('/profile/')
@login_required
def profile():
    """Show a basic profile page including a user's active requests and a signout page."""
    return render_template('profile.html', title="Profile", requests=current_user.requests)
    

@app.route('/logout/')
@login_required
def logout():
    """Log the user out of the current session and return to the homepage."""
    logout_user()

    return redirect('index')


@app.route('/request/<request_id>/')
@login_required
def view_request(request_id):
    """Render the specified request if it belongs to the logged-in user."""
    current_request = Request.query.get(int(request_id))
    
    # Store the current request as a cookie in the session so that it can be accepted or deleted in a different page.
    session['current_request_id'] = request_id
    
    if current_user.is_creator or current_request.user_id == current_user.id:
        return render_template('view_request.html', title=current_request.title, current_request=current_request)
    else:
        return redirect(url_for('profile'))


@app.route('/accept_request/')
@login_required
def accept_request():
    current_request = Request.query.get(int(session['current_request_id']))

    if current_user.is_creator and len(list(current_user.requests)) < 3:
        current_user.requests.append(current_request)
        db.session.commit()
    
    return redirect('profile')
        
        
@app.route('/delete_request/')
@login_required
def delete_request():
    """Delete the specified request if it belongs to the currently logged in user."""
    current_request = Request.query.get(int(session['current_request_id']))

    if current_request.user_id == current_user.id:
        db.session.delete(current_request)
        db.session.commit()

    return redirect(url_for('profile'))
