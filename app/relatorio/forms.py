from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class RelatorioForm(FlaskForm):
    submitMinhasHoras = SubmitField('Minhas Horas Trabalhadas')
    submitHoras = SubmitField('Horas Trabalhadas')

