from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.auth.forms import ProfileForm
from app.talks.forms import TalkForm
from . import talks
from ..models import User, Talk


@talks.route('/')
def index():
    talk_list = Talk.query.order_by(Talk.date.desc()).all()
    return render_template('talks/index.html', talks=talk_list)

@talks.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    talk_list = user.talks.order_by(Talk.date.desc()).all()
    return render_template('talks/user.html', user=user, talks = talk_list)

@talks.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('talks.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template('talks/profile.html', form=form)

@talks.route('/new', methods=['GET', 'POST'])
@login_required
def new_talk():
    form = TalkForm()
    if form.validate_on_submit():
        talk = Talk(author=current_user)
        form.to_model(talk)
        db.session.add(talk)
        db.session.commit()
        flash('The talk was added successfully.')
        return redirect(url_for('.index'))
    return render_template('talks/edit_talk.html', form=form)

@talks.route('/talk/<int:id>', methods=['GET', 'POST'])
def talk(id):
    talk = Talk.query.get_or_404(id)
    headers = {}
    if current_user.is_authenticated:
        headers['X-XSS-Protection'] = '0'
    return render_template('talks/talk.html', talk=talk),\
           200, headers
