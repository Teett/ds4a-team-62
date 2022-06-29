
import psycopg2
from env.cons import Constantes

class Connection:
    def connect():
        try:
            connection = psycopg2.connect(
                user=Constantes.user,
                password=Constantes.password,
                host=Constantes.host,
                port=Constantes.port,
                database=Constantes.database
            )
            return connection
        except psycopg2.Error as e:
            diagnostico=e.diag.severity
            mensaje=e.diag.message_primary
            print(diagnostico ,mensaje)
            return diagnostico+mensaje

    def closeConnection( connection):
        connection.close()

