from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class ProjetosForm(FlaskForm):
    codigo = StringField('Cod Projeto')
    nomeProjeto = StringField('Nome Projeto')
    cliente = SelectField(
        'Cliente',
        choices=[('Cliente1', 'Cliente1'), ('Cliente2', 'Cliente2'), ('Cliente3', 'Cliente3')])
    descricaoProjeto = StringField('Descrição Projeto')
    submit = SubmitField('Salvar')

