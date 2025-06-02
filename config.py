import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (si existe)
load_dotenv()

# Obtener la ruta base del proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '104070'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Podríamos añadir más configuraciones aquí a medida que las necesitemos
    # Ejemplo:
    # DEBUG = True # O leerlo de una variable de entorno
    #user=admin_pollos
    #password=Poll0Monti3l#2024