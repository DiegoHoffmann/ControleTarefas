from flask import render_template
from .forms import FuncionarioForm
from . import funcionario


@funcionario.route('/funcionario')
def funcionario():
    form = FuncionarioForm()
    return render_template('funcionario/funcionarioCadastro.html', form=form)
