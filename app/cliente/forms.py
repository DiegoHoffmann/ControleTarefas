from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class ClienteForm(FlaskForm):
    cpfCnpj = StringField('Cpf/Cnpj')
    nome = StringField('Nome')
    submit = SubmitField('Cadastrar')


