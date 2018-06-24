from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from app.models import Atividade


class AtividadeForm(FlaskForm):
    projeto = Atividade()
    descricao = StringField('Descrição')
    submit = SubmitField('Cadastrar')


