
from .connection import Connection
from .aws import aws
from .queries import queries
from flask import request, jsonify,json
from env.cons import Constantes

from datetime import datetime , timedelta,date
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

def consulta_admisiones():


    sql="""select * from public.admisions
            """
    data = queries.consultaGeneral(sql)

    return jsonify(data)

def consulta_admisiones_de_hoy():

    now = date.today()
    print(now)
    sql="""select * from public.admisions
            where "currentDate"=%s;
            """
    parametros=(now,)
    data = queries.consultaGeneral(sql,parametros)

    return jsonify(data)

def consulta_admision_por_nombre():
    jsoncr=request.json
    nombre=jsoncr['nombre']
    
    sql="""select * from public.admisions
            where "nombreArchivo"=%s;
            """
    parametros=(nombre,)
    data = queries.consultaGeneral(sql,parametros)
    return jsonify(data)


def insertar_admisions():

    jsoncrArray=request.json
    for jsoncr in jsoncrArray:
        Site=jsoncr['Site']
        DayWeek_coded=jsoncr['DayWeek_coded']
        Shift_coded=jsoncr['Shift_coded'],
        Arr_Amb=jsoncr['Arr_Amb']
        Gender=jsoncr['Gender'],
        Age_band=jsoncr['Age_band']
        IMD_quintile=jsoncr['IMD_quintile']
        Ethnicity=jsoncr['Ethnicity']
        ACSC=jsoncr['ACSC']
        Consultant_on_duty=jsoncr['Consultant_on_duty']
        ED_bed_occupancy=jsoncr['ED bed occupancy']
        Inpatient_beoccupancy=jsoncr['Inpatient_bed_occupancy']
        Arrival_intensity=jsoncr['Arrival intensity']
        LAS_intensity=jsoncr['LAS intensity']
        LWBS_intensity=jsoncr['LWBS intensity']
        Last_10_mins=jsoncr['Last_10_mins']
        nombreArchivo=jsoncr['nombreArchivo']
    consulta=""" ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

    sql="""INSERT INTO public.admisions(
	"Site", "DayWeek_coded", "Shift_coded", "Arr_Amb", "Gender", "Age_band", "IMD_quintile", "Ethnicity", "ACSC", "Consultant_on_duty", "ED bed occupancy", "Inpatient_beoccupancy", "Arrival intensity", "LAS intensity", "LWBS intensity",  "Last_10_mins",   "nombreArchivo")
	VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
    parameters=(Site, DayWeek_coded, Shift_coded, Arr_Amb, Gender, Age_band, IMD_quintile, Ethnicity, ACSC, Consultant_on_duty, ED_bed_occupancy, Inpatient_beoccupancy, Arrival_intensity, LAS_intensity, LWBS_intensity,  Last_10_mins,  nombreArchivo)

    data = queries.updateOrInsert(sql,parameters)

    return jsonify(data)


def insertar_all_admisions():

    jsoncrArray=request.json
    # print(jsoncrArray)
    consulta=""
    for i,jsoncr in enumerate(jsoncrArray):
        Site=jsoncr['Site']
        DayWeek_coded=jsoncr['DayWeek_coded']
        Shift_coded=jsoncr['Shift_coded'],
        Arr_Amb=jsoncr['Arr_Amb']
        Gender=jsoncr['Gender'],
        Age_band=jsoncr['Age_band']
        IMD_quintile=jsoncr['IMD_quintile']
        Ethnicity=jsoncr['Ethnicity']
        ACSC=jsoncr['ACSC']
        Consultant_on_duty=jsoncr['Consultant_on_duty']
        ED_bed_occupancy=jsoncr['ED bed occupancy']
        Inpatient_beoccupancy=jsoncr['Inpatient_bed_occupancy']
        Arrival_intensity=jsoncr['Arrival intensity']
        LAS_intensity=jsoncr['LAS intensity']
        LWBS_intensity=jsoncr['LWBS intensity']
        Last_10_mins=jsoncr['Last_10_mins']
        nombreArchivo=jsoncr['nombreArchivo']

        # print("IMD_quintile ",type(IMD_quintile))
        # print("IMD_quintile ",IMD_quintile)

        consulta=consulta+"""( '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') , """.format(Site, DayWeek_coded, Shift_coded[0], Arr_Amb, Gender[0], Age_band, IMD_quintile, Ethnicity, ACSC, Consultant_on_duty, ED_bed_occupancy, Inpatient_beoccupancy, Arrival_intensity, LAS_intensity, LWBS_intensity,  Last_10_mins,  nombreArchivo)
  
        
    consulta=consulta[:-2]+';'
    # print(consulta)
    sql="""INSERT INTO public.admisions(
	"Site", "DayWeek_coded", "Shift_coded", "Arr_Amb", "Gender", "Age_band", "IMD_quintile", "Ethnicity", "ACSC", "Consultant_on_duty", "ED bed occupancy", "Inpatient_beoccupancy", "Arrival intensity", "LAS intensity", "LWBS intensity",  "Last_10_mins",   "nombreArchivo")
	VALUES {} """.format(consulta)
    print(sql)
    data = queries.updateOrInsert(sql)

    return jsonify(data)