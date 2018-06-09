from flask import Blueprint
projetos = Blueprint('projetos', __name__)
from . import routes

