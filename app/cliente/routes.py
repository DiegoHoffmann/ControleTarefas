from flask import render_template
from .forms import ClienteForm
from . import cliente


@cliente.route('/cliente')
def cliente():
    form = ClienteForm()
    return render_template('cliente/clienteCadastro.html', form=form)
