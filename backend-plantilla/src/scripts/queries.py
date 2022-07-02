from env.cons import Constantes
from .connection import Connection
import psycopg2

class queries:
    def consultaGeneral(sql,parameters=''):
        msm=Constantes.PETICION_REGISTRO_VACIO
        try:
            conn = Connection.connect()
            cursor=conn.cursor()
            if parameters=='':
                cursor.execute(sql) 
            else:
                cursor.execute(sql,parameters)  
            Datos=cursor.fetchall()
            conn.commit()
            cursor.close()
            Connection.closeConnection(conn)
        except psycopg2.Error as e:
            cursor.close()
            Connection.closeConnection(conn)
            diagnostico=e.diag.severity
            mensaje=e.diag.message_primary
            msm=Constantes.ERROR_SERVICIO
        


            data={
                "msm":msm,
                'Respuesta':diagnostico+': '+mensaje
                
                }
            return data

        serial=[]
        for j,dato in enumerate(Datos):
            response={}
            for i, value in enumerate(dato):
                response[cursor.description[i][0]]=value
            serial.append(response)
            msm=Constantes.PETICION_SERVICIO_EXITOSO
        
        if serial==[]:
            response={}
            for i,value in enumerate(cursor.description):
                response[cursor.description[i][0]]=0
            serial.append(response)

        data={"msm":msm,
            'Respuesta':serial
            }
        return data

    def updateOrInsert(sql,parameters=''):
        try:    
            conn = Connection.connect()
            cursor=conn.cursor()
            if parameters=='':
                cursor.execute(sql) 
            else:
                cursor.execute(sql,parameters)  
            conn.commit()
            cursor.close()
            Connection.closeConnection(conn)
            msm=Constantes.PETICION_SERVICIO_EXITOSO
            
        except psycopg2.Error as e:
            
            cursor.close()
            Connection.closeConnection(conn)
            diagnostico= str(e.diag.severity)
            mensaje=str(e.diag.message_primary)
            msm=Constantes.ERROR_SERVICIO
            data={
                "msm":msm,
                'Respuesta':diagnostico+': '+mensaje
                }

            return data
            
        data={"msm":msm,
              'Respuesta':'200'
            }
        return data


