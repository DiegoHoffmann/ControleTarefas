#!/usr/bin/env python
import os

from flask_migrate import Migrate, MigrateCommand
from app import create_app
from flask_script import Manager
from app import db
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def adduser(email, username, admin):
    """ Registra um novo usuário """
    from getpass import getpass
    if admin != "True" and admin != "False":
        import sys
        sys.exit('Terceiro parametro deve ser True or False')
    password = getpass()
    password2 = getpass(prompt="Confirme: ")
    if admin:
        eh_adm = True
    else:
        eh_adm = False

    if password != password2:
        import sys
        sys.exit('Erro: senhas nao conferem')
    db.create_all()
    user = User(email=email, username=username, password=password, is_admin=eh_adm)
    db.session.add(user)
    db.session.commit()
    print('Usuario {0} foi registrado com sucesso.'.format(username) )

if __name__ == '__main__':
    manager.run()


