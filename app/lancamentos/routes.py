from flask import render_template, flash
from .forms import LancamentosForm
from . import lancamentos
from app.models import LancamentoHoras

@lancamentos.route('/lancamentos')
def lancamentos():
    form = LancamentosForm()
    if form.validate_on_submit():
        lanc = LancamentoHoras()
        flash("Ok")
    return render_template('lancamentos/lancamentosCadastro.html', form=form)
