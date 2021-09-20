import hashlib
from datetime import datetime

from flask import request

from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(256))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    bio = db.Column(db.Text)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(256))
    talks = db.relationship('Talk', lazy='dynamic', backref='author')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if (self.email is not None) and (self.avatar_hash is None):
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def passwordAtualizar(password):
        return generate_password_hash(password)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(url=url, hash=hash, size=size, default=default, rating=rating)

class Talk(db.Model):
    __tablename__ = 'talks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    slides = db.Column(db.Text())
    video = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    venue = db.Column(db.String(128))
    venue_url = db.Column(db.String(128))
    date = db.Column(db.DateTime())


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    cpf_cnpj = db.Column(db.Integer, nullable=False, unique=True, index=True)
    nome = db.Column(db.String(40))


class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    matricula = db.Column(db.Integer, unique=True, autoincrement=True)
    nome = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    senha = db.Column(db.String(256))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def password(self, password):
        self.senha = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.senha, password)

class Projeto(db.Model):
    __tablename__= 'projeto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.Text())
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    descricao = db.Column(db.Text())
    #situacao = db.Column(db.Boolean())
    clientes = db.relationship('Cliente', backref="clientes", lazy=True)

class Atividade(db.Model):
    __tablename__= 'atividade'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.Text())


class FuncionarioProjeto(db.Model):
    __tablename__= 'funcionario_projeto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'))
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'))
    cordenador = db.Column(db.Boolean())
    funcionarios = db.relationship('Funcionario', backref="funcionarios", lazy=True)
    projetos = db.relationship('Projeto', backref="projetos", lazy=True)

class LancamentoHoras(db.Model):
    __tablename__ = 'lancamento_horas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_hora_inicio = db.Column(db.DateTime)
    data_hora_fim = db.Column(db.DateTime)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividade.id'))
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id'))
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'))
    descricao = db.Column(db.Text())
    funcionarios = db.relationship('Funcionario', backref="funcionariosHoras", lazy=True)
    projetos = db.relationship('Projeto', backref="projetosHoras", lazy=True)
    atividades = db.relationship('Atividade', backref="atividadesHoras", lazy=True)

class Ponto(db.Model):
    __tablename__ = 'ponto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_lancamento = db.Column(db.Date)
    hora_inicio_1 = db.Column(db.DateTime)
    hora_fim_1 = db.Column(db.DateTime)
    hora_inicio_2 = db.Column(db.DateTime)
    hora_fim_2 = db.Column(db.DateTime)
    hora_inicio_3 = db.Column(db.DateTime)
    hora_fim_3 = db.Column(db.DateTime)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'))
    funcionarios = db.relationship('Funcionario', backref="funcionariosPonto", lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

