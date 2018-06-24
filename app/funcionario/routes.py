from operator import or_

from flask import render_template, flash, redirect, url_for, request
from .forms import FuncionarioForm
from . import funcionario
from app.models import Funcionario, db


@funcionario.route('/funcionario', methods=['GET', 'POST'])
def criarFuncionario():
    form = FuncionarioForm()

    if form.validate_on_submit():
        funcionario = Funcionario()
        funcionario.nome = form.nome.data.upper()
        funcionario.matricula = form.matricula.data
        funcionario.password(form.senha.data)

        db.session.add(funcionario)
        db.session.commit()

        flash("Funcionário inserido com sucesso!")
        return redirect(url_for('.criarFuncionario'))
    else:
        return render_template('funcionario/funcionarioCadastro.html', form=form)

@funcionario.route('/lista',methods=['GET','POST'])
def funcionarioLista():
    funcionarioLista = Funcionario.query.all()
    if request.form.get('submitFiltro') == 'submitFiltro':
        filtro = request.form.get('txtFiltro')
        if filtro is None or filtro == "":
            funcionarioLista = Funcionario.query.all()
        else:
            funcionarioLista = Funcionario.query.filter(or_(Funcionario.matricula.like('%' + filtro + '%'),
                                                        Funcionario.nome.like('%' + filtro + '%')))

    else:
        funcionarioLista = Funcionario.query.all()
    return render_template('funcionario/funcionarioCadastroLista.html', funcionarioLista=funcionarioLista)