from flask import render_template, flash, request, url_for, session
from werkzeug.utils import redirect

from app import db
from app.models import User
from .forms import PerfilForm
from . import perfil


@perfil.route('/carregarperfil')
def carregarPerfil():
    form = PerfilForm()
    return render_template('perfil/perfilCadastro.html', form=form)

@perfil.route('/alterarSenha', methods=['GET','POST'])
def alterarSenha():
    form = PerfilForm()
    return render_template('perfil/alterarSenha.html', form=form)


@perfil.route('/alterarSenha/salvar', methods=['GET','POST'])
def alterarSenhaSalvar():
    if request.form.get('salvar') == 'Salvar':
        user = User.query.filter_by(email=session["session_name"]).first()
        senhaAnterior = request.form.get('txtSenhaAnterior')
        if user.verify_password(senhaAnterior):
            #db.session.query(Ponto).filter(Ponto.id == temPonto.id).update({Ponto.hora_fim_3: datetime.now()})
            if request.form.get('txtNovaSenha') == request.form.get('txtConfirmaSenha'):
                novaSenha = request.form.get('txtNovaSenha')
                if len(novaSenha) < 4:
                    flash("Senha muito fraca")
                    return redirect(url_for('.alterarSenha'))
                else:
                    db.session.query(User).filter(User.id == user.id).update({User.password_hash: User.passwordAtualizar(novaSenha)})
                    db.session.commit()
                    flash("Senha alterada com sucesso")

            else:
                flash("Confirmação de senha invalida")

    return redirect(url_for('.alterarSenha'))