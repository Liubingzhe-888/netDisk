from flask import Blueprint

API2 = Blueprint('api_2_0',__name__,static_folder='static')

from . import api,login,share