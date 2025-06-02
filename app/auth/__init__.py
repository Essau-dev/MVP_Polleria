from flask import Blueprint

bp = Blueprint('auth', __name__)

# Importar rutas al final para evitar importaciones circulares
from app.auth import routes