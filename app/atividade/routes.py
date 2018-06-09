from flask import render_template
from .forms import AtividadeForm
from . import atividade


@atividade.route('/atividade')
def atividade():
    form = AtividadeForm()
    return render_template('atividade/atividadeCadastro.html', form=form)
