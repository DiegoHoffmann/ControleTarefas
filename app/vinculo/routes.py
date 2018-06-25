from operator import or_

from flask import render_template, redirect, url_for, flash, request
from .forms import VinculoForm
from . import vinculo
from app.models import FuncionarioProjeto, db, Funcionario, Projeto


@vinculo.route('/vinculo', methods=['GET', 'POST'])
def criarVinculo():
    form = VinculoForm()
    form.codigoProjeto.choices = [(c.id, c.nome) for c in Projeto.query.all()]
    form.codigoProjeto.choices.insert(0, [0, "SELECIONE"])
    form.codigoFuncionario.choices = [(c.id, c.nome) for c in Funcionario.query.all()]
    form.codigoFuncionario.choices.insert(0,[0,"SELECIONE"])
    if form.validate_on_submit():
        funcProj = FuncionarioProjeto()
        funcProj.funcionario_id = form.codigoFuncionario.data
        funcProj.projeto_id = form.codigoProjeto.data
        funcProj.cordenador = form.cordenador.data
        db.session.add(funcProj)
        db.session.commit()
        flash("Viculo inserido com sucesso")
        return redirect(url_for('.criarVinculo'))
    else:
        return render_template('vinculo/vinculoCadastro.html', form=form)

@vinculo.route('/lista',methods=['GET', 'POST'])
def vinculoLista():
    if request.form.get('submitFiltro') == 'submitFiltro':
        filtro = request.form.get('txtFiltro')
        filtroCordenador = request.form.get('chkCordenador')
        filtroFuncionario = request.form.get('chkFuncionario')
        if filtroCordenador == "on":
            buscaCordenador = True
        else:
            buscaCordenador = False

        if filtroFuncionario == "on":
            buscaFuncionario = False
        else:
            buscaFuncionario = True

        if filtro is None or filtro == "":
            if buscaCordenador or not buscaFuncionario :
                vinculoLista = FuncionarioProjeto.query.filter(or_(FuncionarioProjeto.cordenador == buscaCordenador, FuncionarioProjeto.cordenador == buscaFuncionario))
            else:
                vinculoLista = FuncionarioProjeto.query.all()
        else:
            vinculoLista = FuncionarioProjeto.query.join(FuncionarioProjeto.funcionarios)\
                .join(FuncionarioProjeto.projetos)\
                .filter(or_(Funcionario.nome.like('%' + filtro +'%'),Funcionario.matricula.like('%' + filtro +'%')) | \
                           (Projeto.nome.like('%' + filtro +'%')), ((FuncionarioProjeto.cordenador == buscaCordenador) | (FuncionarioProjeto.cordenador == buscaFuncionario)))


    else:
        vinculoLista = FuncionarioProjeto.query.all()


    return render_template('vinculo/vinculoCadastroLista.html', vinculoLista=vinculoLista)


@vinculo.route('/lista/remover',methods=['GET', 'POST'])
def vinculoListaRemover():
    idRegistro =request.form.get('remover')
    if request.form.get('remover') is not None:
        vinculo = FuncionarioProjeto.query.filter(FuncionarioProjeto.id == idRegistro).first()
        db.session.delete(vinculo)
        db.session.commit()
        flash("Viculo removido com sucesso")

    return redirect(url_for('.vinculoLista'))