from flask import Blueprint
from . import controllers

primavera = Blueprint('primavera', __name__)


primavera.add_url_rule('/', view_func=controllers.a,methods=['GET'])

controllers.prueba.methods = ['GET']
primavera.add_url_rule(
    '/prueba', view_func=controllers.prueba)


primavera.add_url_rule('/parameters', view_func=controllers.parameters,methods=['POST'])

