from flask import Blueprint
cliente = Blueprint('cliente', __name__)
from . import routes

