from operator import or_

from flask import render_template, flash, redirect, url_for, request
from sqlalchemy import exc

from .forms import ClienteForm
from . import cliente
from app.models import Cliente, db

@cliente.route('/', methods=['GET', 'POST'])
def criarCliente():
    form = ClienteForm()
    if form.validate_on_submit():
        try:
            cliente = Cliente()
            cliente.cpf_cnpj = form.cpfCnpj.data
            cliente.nome = form.nome.data.upper()
            db.session.add(cliente)
            db.session.commit()
            form.data.clear()
            flash("Cliente inserido com sucesso!")
            return redirect(url_for('.criarCliente'))

        except:
            if exc.IntegrityError:
                flash("Cliente já cadastrado!")
                return redirect(url_for('.criarCliente'))
    else:
        return render_template('cliente/clienteCadastro.html', form=form)

@cliente.route('/lista', methods=['GET', 'POST'])
def clienteLista():
    clienteLista = Cliente.query.all()
    if request.form.get('submitFiltro') == 'submitFiltro':
        filtro = request.form.get('txtFiltro')
        if filtro is None or filtro == "":
            clienteLista = Cliente.query.all()
        else:
            clienteLista = Cliente.query.filter(or_(Cliente.cpf_cnpj.like('%' + filtro + '%'),
                                                    Cliente.nome.like('%' + filtro + '%')))

    else:
        clienteLista = Cliente.query.all()

    return render_template('cliente/clienteCadastroLista.html', clienteLista=clienteLista)