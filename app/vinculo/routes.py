from flask import render_template
from .forms import VinculoForm
from . import vinculo


@vinculo.route('/vinculo')
def vinculo():
    form = VinculoForm()
    return render_template('vinculo/vinculoCadastro.html', form=form)
