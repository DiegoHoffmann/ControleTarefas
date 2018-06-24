from operator import or_

from flask import render_template, redirect, request, url_for, flash
from .forms import AtividadeForm
from . import atividade
from app.models import Atividade, db


@atividade.route('/', methods=['GET', 'POST'])
def criarAtividade():
    form = AtividadeForm()
    if form.validate_on_submit():
        ativ = Atividade()
        ativ.descricao = form.descricao.data
        db.session.add(ativ)
        db.session.commit()
        flash("Atividade inserida com sucesso")
        return redirect(url_for('.criarAtividade'))
    else:

        return render_template('atividade/atividadeCadastro.html', form=form)



@atividade.route('/lista', methods=['GET','POST'])
def atividadeLista():
    if request.form.get('submitFiltro') == 'submitFiltro':
        filtro = request.form.get('txtFiltro')
        if filtro is None or filtro == "":
            atividadeLista = Atividade.query.all()
        else:
            atividadeLista = Atividade.query.filter(or_(Atividade.id.like('%' + filtro + '%'),
                                                        Atividade.descricao.like('%' + filtro + '%')))
    else:
        atividadeLista = Atividade.query.all()

    return render_template('atividade/atividadeCadastroLista.html', atividadeLista=atividadeLista)
