from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged In')
    submit = SubmitField('Log In')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    location = StringField('Location', validators=[DataRequired(), Length(1,64)])
    bio = TextAreaField('Bio', validators=[DataRequired()])