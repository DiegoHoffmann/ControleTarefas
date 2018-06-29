from flask import render_template
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