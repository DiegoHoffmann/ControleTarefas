from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

bootstrap = Bootstrap
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from .talks import talks as talks_blueprint
    app.register_blueprint(talks_blueprint)

    # Inicializando app Bootstrap
    bootstrap(app)

    # Inicializando Database
    db.init_app(app)

    # Inicializando Autenticacao
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    login_manager.init_app(app)

    from .cliente import cliente as cliente_blueprint
    app.register_blueprint(cliente_blueprint, url_prefix='/admin')

    from .funcionario import funcionario as funcionario_blueprint
    app.register_blueprint(funcionario_blueprint, url_prefix='/admin')

    from .projetos import projetos as projetos_blueprint
    app.register_blueprint(projetos_blueprint, url_prefix='/admin')

    from .vinculo import vinculo as vinculo_blueprint
    app.register_blueprint(vinculo_blueprint, url_prefix='/admin')

    from .atividade import atividade as atividade_blueprint
    app.register_blueprint(atividade_blueprint, url_prefix='/admin')

    from .lancamentos import lancamentos as lancamentos_blueprint
    app.register_blueprint(lancamentos_blueprint, url_prefix='/lancamentos')

    from .relatorio import relatorio as relatorio_blueprint
    app.register_blueprint(relatorio_blueprint, url_prefix='/relatorio')

    from .perfil import perfil as perfil_blueprint
    app.register_blueprint(perfil_blueprint, url_prefix='/perfil')
    return app



