from flask import Flask, url_for, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
from datetime import datetime
from markupsafe import Markup # Importar Markup

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

    from app import models

    # --- Registrar Blueprints ---
    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.productos import bp as productos_bp
    app.register_blueprint(productos_bp, url_prefix='/productos')

    # Añadir filtro personalizado para formatear fechas en Jinja2
    @app.template_filter('date_format')
    def format_date(value, format='%Y'):
        if value is None:
            return ""
        if isinstance(value, str) and value.lower() == 'now':
            value = datetime.utcnow()
        elif isinstance(value, str):
             try:
                 value = datetime.fromisoformat(value)
             except ValueError:
                 return value
        if isinstance(value, datetime):
             return value.strftime(format)
        else:
             return str(value)

    # Añadir filtro personalizado para nl2br (newline to break)
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if s is None:
            return ""
        # Reemplaza saltos de línea con <br> y marca como seguro para HTML
        return Markup(str(s).replace('\n', '<br>\n'))


    # Modificamos la página de inicio para que use una plantilla
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    return app
