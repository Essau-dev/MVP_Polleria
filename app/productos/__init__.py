from flask import Blueprint

bp = Blueprint(
    'productos', __name__, 
    #template_folder='templates'
    url_prefix='/productos'
    )

# Importar rutas al final para evitar importaciones circulares
from app.productos import routes