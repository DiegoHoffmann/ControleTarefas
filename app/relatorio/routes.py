from flask import render_template
from .forms import RelatorioForm
from . import relatorio


@relatorio.route('/relatorio')
def relatorio():
    form = RelatorioForm()
    return render_template('relatorio/relatorioCadastro.html', form=form)
