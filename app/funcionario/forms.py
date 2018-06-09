from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class FuncionarioForm(FlaskForm):
    matricula = StringField('Matricula')
    nome = StringField('Nome')
    senha = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Salvar')

