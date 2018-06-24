from operator import or_

from flask import render_template, flash, url_for, request
from werkzeug.utils import redirect

from .forms import ProjetosForm
from . import projetos
from app.models import Projeto, db, Cliente

@projetos.route('/', methods=['GET', 'POST'])
def criarProjetos():
    form = ProjetosForm()
    form.cliente.choices = [(c.id, c.nome) for c in Cliente.query.all()]
    form.cliente.choices.insert(0,[0,"SELECIONE"])
    if form.validate_on_submit():
        proj = Projeto()
        proj.nome = form.nomeProjeto.data.upper()
        proj.cliente_id = form.cliente.data
        proj.descricao = form.descricaoProjeto.data
        db.session.add(proj)
        db.session.commit()

        flash("Projeto incluido com sucesso!")
        return redirect(url_for('.criarProjetos'))
    else:
        return render_template('projetos/projetosCadastro.html', form=form)

@projetos.route('/lista', methods=['GET', 'POST'])
def projetoLista():
    if request.form.get('submitFiltro') == 'submitFiltro':
        filtro = request.form.get('txtFiltro')
        if filtro is None or filtro == "":
            projetoLista = Projeto.query.all()
        else:
            projetoLista = Projeto.query.filter(or_(Projeto.id.like('%' + filtro + '%'),
                                                    Projeto.nome.like('%' + filtro + '%')) |
                                                    Projeto.descricao.like('%' + filtro + '%'))

    else:
        projetoLista = Projeto.query.all()

    return render_template('projetos/projetosCadastroLista.html', projetoLista=projetoLista)

