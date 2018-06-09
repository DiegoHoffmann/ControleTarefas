from flask import Blueprint
funcionario = Blueprint('funcionario', __name__)
from . import routes

