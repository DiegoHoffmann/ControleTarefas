from flask import render_template
from .forms import ProjetosForm
from . import projetos


@projetos.route('/projetos')
def projetos():
    form = ProjetosForm()
    return render_template('projetos/projetosCadastro.html', form=form)
