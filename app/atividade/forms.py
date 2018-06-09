from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AtividadeForm(FlaskForm):
    codigo = StringField('Cod Atividade')
    descricao = StringField('Descrição')
    submit = SubmitField('Cadastrar')


