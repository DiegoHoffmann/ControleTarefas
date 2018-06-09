from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class LancamentosForm(FlaskForm):
    codigo = SelectField(
        'Projeto',
        choices=[('Projeto1', 'Projeto1'), ('Projeto2', 'Projeto2'), ('Projeto3', 'Projeto3')])

    submit = SubmitField('Cadastrar')


