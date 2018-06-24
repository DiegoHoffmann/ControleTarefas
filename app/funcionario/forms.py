from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired


class FuncionarioForm(FlaskForm):
    matricula = StringField('Matricula', validators=[validators.required(), validators.Length(max=10, message="Limite de 10 caracteres")])
    nome = StringField('Nome')
    senha = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

