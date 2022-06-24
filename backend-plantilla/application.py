from src.settings import application
from src.scripts.routes import primavera

# Aplicaciones
application.register_blueprint(primavera)

if __name__ == '__main__':
    application.run(debug = True,host='0.0.0.0',port=5000)
    