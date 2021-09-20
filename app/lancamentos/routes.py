from datetime import datetime
from flask import render_template, flash, session, request, url_for,redirect

from .forms import LancamentosForm
from . import lancamentos
from app.models import LancamentoHoras, db, Atividade, Projeto, Funcionario, User, Ponto, FuncionarioProjeto


@lancamentos.route('/')
def carregarLancamentos():
    user = User.query.filter_by(email=session["session_name"]).first_or_404()
    funcionario = Funcionario.query.filter(Funcionario.matricula == user.id).first()
    atividade = Atividade.query.all()
    projeto = FuncionarioProjeto.query.join(FuncionarioProjeto.projetos).filter(FuncionarioProjeto.funcionario_id == Funcionario.id).all()
    dataHoje = datetime.now().date()
    temPonto = Ponto.query.filter(Ponto.funcionario_id == Funcionario.id, Ponto.data_lancamento == dataHoje).first()
    atividadeLancList = LancamentoHoras.query.join(LancamentoHoras.projetos).join(LancamentoHoras.atividades).filter(\
        LancamentoHoras.funcionario_id == Funcionario.id).order_by(LancamentoHoras.data_hora_inicio)

    return render_template('lancamentos/lancamentosCadastro.html', projetoList=projeto, atividadeList=atividade, temPonto=temPonto, dataHoje=dataHoje, atividadeLancList=atividadeLancList)

@lancamentos.route('/salvarPonto',methods=['GET','POST'])
def salvarPonto():
    user = User.query.filter_by(email=session["session_name"]).first_or_404()
    funcionario = Funcionario.query.filter(Funcionario.matricula == user.id).first()
    if request.form.get('btnInicio') == 'Registrar Ponto':
        dataHoje = datetime.now().date()
        temPonto = Ponto.query.filter(Ponto.funcionario_id == Funcionario.id, Ponto.data_lancamento == dataHoje).first()
        ponto = Ponto()
        if temPonto is not None:
            ponto = temPonto
            ponto.funcionario_id = funcionario.id
            if temPonto.hora_inicio_1 is not None:
                if temPonto.hora_fim_1 is not None:
                    if temPonto.hora_inicio_2 is not None:
                        if temPonto.hora_fim_2 is not None:
                            if temPonto.hora_inicio_3 is not None:
                                if temPonto.hora_fim_3 is not None:
                                    flash("Ih deu treta!")
                                else:
                                    ponto.hora_fim_3 = datetime.now()
                                    db.session.query(Ponto).filter(Ponto.id == temPonto.id).update({Ponto.hora_fim_3: datetime.now()})
                            else:
                                ponto.hora_inicio_3 = datetime.now()
                                db.session.query(Ponto).filter(Ponto.id == temPonto.id).update({Ponto.hora_inicio_3: datetime.now()})
                        else:
                            ponto.hora_fim_2 = datetime.now()
                            db.session.query(Ponto).filter(Ponto.id == temPonto.id).update({Ponto.hora_fim_2: datetime.now()})
                    else:
                        ponto.hora_inicio_2 = datetime.now()
                        db.session.query(Ponto).filter(Ponto.id == temPonto.id).update({Ponto.hora_inicio_2: datetime.now()})
                else:
                    ponto.hora_fim_1 = datetime.now()
                    db.session.query(Ponto).filter(Ponto.id == temPonto.id).update({Ponto.hora_fim_1: datetime.now()})
            else:
                ponto.hora_inicio_1 = datetime.now()
                db.session.query(Ponto).filter(Ponto.id == temPonto.id).update({Ponto.hora_inicio_1: datetime.now()})

            db.session.commit()
        else:
            ponto.data_lancamento = datetime.now().date()
            ponto.hora_inicio_1 = datetime.now()
            ponto.funcionario_id = funcionario.id
            db.session.add(ponto)
            db.session.commit()
        flash("Ponto Lancado")

    return redirect(url_for('.carregarLancamentos'))


@lancamentos.route('/salvarAtividade', methods=['GET', 'POST'])
def salvarAtividade():

    if (request.form.get('selectProjeto') == "0" or request.form.get('selectAtividade') == "0" or request.form.get('txtDescricao') is None):
        flash("Informe os campo corretamente")
        return redirect(url_for('.carregarLancamentos'))
    else:
        try:
            user = User.query.filter_by(email=session["session_name"]).first()
            funcionario = Funcionario.query.filter_by(matricula=user.id).first()
            lancamento = LancamentoHoras()
            lancamento.funcionario_id = funcionario.id
            lancamento.projeto_id = request.form.get('selectProjeto')
            lancamento.atividade_id = request.form.get('selectAtividade')

            dataHora = request.form.get('txtDtInicio') + ' ' + request.form.get('txtHoraInicio') + ":00.000000"
            dataInicio = datetime.strptime(dataHora, "%Y-%m-%d %H:%M:%S.%f")
            dataHora = request.form.get('txtDtFim') + ' ' + request.form.get('txtHoraFim') + ":00.000000"
            dataFim = datetime.strptime(dataHora, "%Y-%m-%d %H:%M:%S.%f")

            if dataInicio > dataFim:
                flash("Informe os campo corretamente Data")
                return redirect(url_for('.carregarLancamentos'), 100, None)

            lancamento.data_hora_inicio = dataInicio
            lancamento.data_hora_fim = dataFim
            lancamento.descricao = request.form.get('txtDescricao')

            db.session.add(lancamento)
            db.session.commit()
            flash("Atividade Lancada")
            return redirect(url_for('.carregarLancamentos'))
        except Exception as e:
            flash("Erro ao incluir Atividade")
            return redirect(url_for('.carregarLancamentos'))

@lancamentos.route('/removerAtividade', methods=['GET', 'POST'])
def removerAtividade():
    flash(request.form.get('remover'))
    if request.form.get('remover') is not None:
        idRegistro = request.form.get('remover')
        lancamento = LancamentoHoras.query.filter(id=idRegistro).first()
        db.session.delete(lancamento)
        db.session.commit()
        flash("Atividade removida com sucesso")
    elif request.form.get('edit') is not None:
        idRegistro = request.form.get('edit')
        return redirect(url_for('.carregarEditarLancamentos', idRegistro=idRegistro))
    return redirect(url_for('.carregarLancamentos'))



@lancamentos.route('/carregarEditarLancamentos/<idRegistro>')
def carregarEditarLancamentos(idRegistro):
    user = User.query.filter_by(email=session["session_name"]).first_or_404()
    funcionario = Funcionario.query.filter(Funcionario.matricula == user.id).first()
    dataHoje = datetime.now().date()
    temPonto = Ponto.query.filter(Ponto.funcionario_id == funcionario.id, Ponto.data_lancamento == dataHoje).first()
    atividadeLancList = LancamentoHoras.query.join(LancamentoHoras.projetos).join(LancamentoHoras.atividades).filter(\
        LancamentoHoras.id == idRegistro).first()
    atividade = Atividade.query.filter(Atividade.id != atividadeLancList.atividade_id).all()
    projeto = FuncionarioProjeto.query.join(FuncionarioProjeto.projetos).filter(
        FuncionarioProjeto.funcionario_id == funcionario.id, FuncionarioProjeto.projeto_id != atividadeLancList.projeto_id).all()
    return render_template('lancamentos/editarLancamentosCadastro.html', projetoList=projeto, atividadeList=atividade, temPonto=temPonto, dataHoje=dataHoje, atividadeLancList=atividadeLancList)


@lancamentos.route('/salvarAlteracaoAtividade', methods=['GET', 'POST'])
def salvarAlteracaoAtividade():

    if (request.form.get('selectProjeto') == "0" or request.form.get('selectAtividade') == "0" or request.form.get('txtDescricao') is None):
        flash("Informe os campo corretamente")
        return redirect(url_for('.carregarLancamentos'))
    else:
        try:
            user = User.query.filter_by(email=session["session_name"]).first_or_404()
            idRegistro = request.form.get('idAtividade')
            funcionario = Funcionario.query.filter(Funcionario.matricula == user.id).first()
            lancamento = LancamentoHoras()
            lancamento.funcionario_id = funcionario.id
            lancamento.projeto_id = request.form.get('selectProjeto')
            lancamento.atividade_id = request.form.get('selectAtividade')

            dataHora = request.form.get('txtDtInicio') + ' ' + request.form.get('txtHoraInicio') + ":00.000000"
            dataInicio = datetime.strptime(dataHora, "%Y-%m-%d %H:%M:%S.%f")
            dataHora = request.form.get('txtDtFim') + ' ' + request.form.get('txtHoraFim') + ":00.000000"
            dataFim = datetime.strptime(dataHora, "%Y-%m-%d %H:%M:%S.%f")

            if dataInicio > dataFim:
                flash("Informe os campo corretamente")
                return redirect(url_for('.carregarLancamentos') )

            lancamento.data_hora_inicio = dataInicio
            lancamento.data_hora_fim = dataFim
            lancamento.descricao = request.form.get('txtDescricao')

            db.session.query(LancamentoHoras).filter(LancamentoHoras.id == idRegistro).\
                update({LancamentoHoras.projeto_id: lancamento.projeto_id,
                        LancamentoHoras.atividade_id: lancamento.atividade_id,
                        LancamentoHoras.data_hora_inicio: lancamento.data_hora_inicio,
                        LancamentoHoras.data_hora_fim: lancamento.data_hora_fim,
                        LancamentoHoras.descricao: lancamento.descricao})
            db.session.commit()
            flash("Atividade Lancada")
            return redirect(url_for('.carregarLancamentos'))
        except:
            flash("Informe os campo corretamente")
            return redirect(url_for('.carregarEditarLancamentos', idRegistro=idRegistro))