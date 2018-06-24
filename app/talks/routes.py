from flask import render_template, url_for, redirect, session
from . import talks
from ..models import User


@talks.route('/')
def index():
    if "session_name" in session and session["session_name"] is not None :
        user = User.query.filter_by(email=session["session_name"]).first_or_404()
        return render_template('talks/user.html', user=user)
    else:
        return redirect(url_for('auth.login'))


@talks.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('talks/user.html', user=user)


