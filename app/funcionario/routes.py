from operator import or_

from flask import render_template, flash, redirect, url_for, request, session
from .forms import FuncionarioForm
from . import funcionario
from app.models import Funcionario, db, User


@funcionario.route('/funcionario', methods=['GET', 'POST'])
def criarFuncionario():
    form = FuncionarioForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=session["session_name"]).first_or_404()
        if user is None:
            usuario = User(email=form.email.data, username=form.nome.data.upper(), password=form.senha.data,
                           is_admin=form.admin.data)

            db.session.add(usuario)
            db.session.commit()
            usuarioCriado = User.query.filter(User.email == form.email.data).first()
        else:
            usuarioCriado = user

        funcionario = Funcionario()
        funcionario.nome = form.nome.data.upper()
        funcionario.user_id = usuarioCriado.id
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