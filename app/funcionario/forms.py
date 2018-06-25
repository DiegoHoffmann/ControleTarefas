from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, BooleanField
from wtforms.validators import DataRequired, Length, Email


class FuncionarioForm(FlaskForm):
    nome = StringField('Nome')
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    senha = PasswordField('Password', validators=[DataRequired()])
    admin = BooleanField('Admin')
    submit = SubmitField('Cadastrar')

