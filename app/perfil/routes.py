from flask import render_template
from .forms import PerfilForm
from . import perfil


@perfil.route('/perfil')
def perfil():
    form = PerfilForm()
    return render_template('perfil/perfilCadastro.html', form=form)
