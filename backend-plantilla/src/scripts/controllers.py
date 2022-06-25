
from .connection import Connection
from .aws import aws
from .queries import queries
from flask import request, jsonify,json
from env.cons import Constantes

from datetime import datetime , timedelta
from os import  remove
import os
import pandas as pd


# import logging

# logging.basicConfig(filename='backendVeticalSalud.log')


def prueba():
    serial=[]
    response=''

 
    sql = "select * from public.prueba;"

    data = queries.consultaGeneral(sql)

    return jsonify(data)

def a():

    data={
        'Respuesta':"cristian"
    }
    
    return jsonify(data)


def parameters():

    jsoncr=request.json
    id=jsoncr['Make']

    sql="""INSERT INTO public.prueba(
             nombre)
            VALUES (%s);
            """
    parameters=(id,)

    data = queries.updateOrInsert(sql,parameters)

    return jsonify(data)



