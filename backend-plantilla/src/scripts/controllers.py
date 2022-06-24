
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

    try:
        conn = Connection.connect()
        cursor=conn.cursor()
        sql = "select * from public.prueba;"
        cursor.execute(sql)  # write the first row of data
        Datos=cursor.fetchall()
        conn.commit()
        cursor.close()
        Connection.closeConnection(conn)
        for i in Datos:
            response = {
                        'id' : i[0],
                        'nombre': i[1],
                        }
        serial.append(response)
    except:
        serial="error conexion"

    data={
        'Respuesta':serial
    }
    return jsonify(data)

def a():

    data={
        'Respuesta':"cristian"
    }
    
    return jsonify(data)


def parameters():

    jsoncr=request.json
    id=jsoncr['id']

    sql="""select * from public.prueba
            where id = %s;
            """
    parameters=(id,)

    data = queries.consultaGeneral(sql,parameters)

    return jsonify(data)



