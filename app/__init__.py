from flask import Flask, url_for, render_template, send_from_directory # Importar send_from_directory
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
from flask_moment import Moment
from datetime import datetime
from markupsafe import Markup
import os # Importar os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = "Por favor, inicia sesión para acceder a esta página."
login.login_message_category = "info"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    moment = Moment(app)

    from app import models

    # --- Registrar Blueprints ---
    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.productos import bp as productos_bp
    app.register_blueprint(productos_bp, url_prefix='/productos')

    # Añadir filtro personalizado para nl2br (newline to break)
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if s is None:
            return ""
        return Markup(str(s).replace('\n', '<br>\n'))

    # Procesador de contexto para hacer 'current_time' disponible en todas las plantillas
    @app.context_processor
    def inject_current_time():
        return {'current_time': datetime.utcnow()}

    # Modificamos la página de inicio para que use una plantilla
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    # --- Nueva ruta para servir sw.js desde la raíz ---
    @app.route('/sw.js')
    def service_worker():
        # Asegúrate de que el archivo sw.js esté en la carpeta 'app'
        return send_from_directory(app.root_path, 'sw.js')
    # --- Fin de la nueva ruta ---

    return app
