from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired


class VinculoForm(FlaskForm):
    codigoFuncionario = SelectField('Funcionario', coerce=int)
    codigoProjeto = SelectField('Cliente', coerce=int)
    cordenador = BooleanField('Cordenador')

    submit = SubmitField('Cadastrar')

