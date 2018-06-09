from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class PerfilForm(FlaskForm):
    funcionario = StringField('Perfil')


