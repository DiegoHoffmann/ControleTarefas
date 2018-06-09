from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class VinculoForm(FlaskForm):
    codigoFuncionarioProjeto = StringField('Funcionario X Projeto')
    codigoFuncionario = SelectField(
        'Funcionario',
        choices=[('Cliente1', 'Cliente1'), ('Cliente2', 'Cliente2'), ('Cliente3', 'Cliente3')])
    codigoProjeto = SelectField(
        'Projeto',
        choices=[('Projeto1', 'Projeto1'), ('Projeto2', 'Projeto2'), ('Projeto3', 'Projeto3')])

    submit = SubmitField('Salvar')

