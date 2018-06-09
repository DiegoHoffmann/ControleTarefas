from flask import render_template
from .forms import LancamentosForm
from . import lancamentos


@lancamentos.route('/lancamentos')
def lancamentos():
    form = LancamentosForm()
    return render_template('lancamentos/lancamentosCadastro.html', form=form)
