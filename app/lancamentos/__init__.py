from flask import Blueprint
lancamentos = Blueprint('lancamentos', __name__)
from . import routes

