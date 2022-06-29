from flask import Flask
from flask_cors import CORS

class Settings:
    DEBUG = True  # para desarrollo
    ENV = "development"

application = Flask(__name__)
application.config.from_object(Settings)
CORS(application)
