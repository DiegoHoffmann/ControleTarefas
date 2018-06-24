from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class ProjetosForm(FlaskForm):
    nomeProjeto = StringField('Nome Projeto')
    cliente = SelectField('Cliente', coerce=int)
    descricaoProjeto = StringField('Descrição Projeto')
    submit = SubmitField('Cadastrar')
