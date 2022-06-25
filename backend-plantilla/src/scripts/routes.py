from flask import Blueprint
from . import controllers

primavera = Blueprint('primavera', __name__)


primavera.add_url_rule('/', view_func=controllers.a,methods=['GET'])

controllers.prueba.methods = ['GET']
primavera.add_url_rule(
    '/prueba', view_func=controllers.prueba)


primavera.add_url_rule('/parameters', view_func=controllers.parameters,methods=['POST'])

primavera.add_url_rule('/consulta_admisiones', view_func=controllers.consulta_admisiones,methods=['GET'])

primavera.add_url_rule('/consulta_admisiones_de_hoy', view_func=controllers.consulta_admisiones_de_hoy,methods=['GET'])

primavera.add_url_rule('/consulta_admision_por_nombre', view_func=controllers.consulta_admision_por_nombre,methods=['GET'])

primavera.add_url_rule('/insertar_admisions', view_func=controllers.insertar_admisions,methods=['POST'])



