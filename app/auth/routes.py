from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm
from app.models import Usuario # Mantener la importación si se usa el tipo Usuario directamente
# from datetime import datetime # Ya no es necesario importar datetime aquí
from urllib.parse import urlsplit # Para el next_page
from app.auth import services # Importar el módulo de servicios

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está autenticado, redirigir a la página principal o dashboard
    if current_user.is_authenticated:
        return redirect(url_for('index')) # O url_for('dashboard')

    form = LoginForm()
    if form.validate_on_submit():
        # Usar la función de servicio para obtener el usuario
        user = services.obtener_usuario_por_username(form.username.data)

        # Verificar si el usuario existe y la contraseña es correcta
        if user is None or not user.check_password(form.password.data):
            flash('Nombre de usuario o contraseña inválidos.', 'danger')
            return redirect(url_for('auth.login'))

        # Si la autenticación es exitosa
        login_user(user, remember=form.remember_me.data)

        # Actualizar la fecha del último login usando el servicio
        try:
            services.actualizar_ultimo_login(user)
            db.session.commit() # Confirmar la transacción
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar ultimo_login para {user.username}: {e}")
            # Considera si quieres mostrar un flash message aquí o solo loguear el error

        # Redirigir a la página 'next' si existe, de lo contrario a la página principal
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index') # O url_for('dashboard')

        flash(f'¡Bienvenido, {user.nombre_completo}!', 'success')
        return redirect(next_page)

    return render_template('auth/login.html', title='Iniciar Sesión', form=form)

@bp.route('/logout')
@login_required # Asegurarse que solo usuarios logueados puedan desloguearse
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('index'))

# Podríamos añadir rutas para registro, reseteo de contraseña, etc. aquí en el futuro.