from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm
from app.models import Usuario
from datetime import datetime # Para actualizar ultimo_login
from urllib.parse import urlsplit # Para el next_page

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) # O a un dashboard si ya está logueado

    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña inválidos.', 'danger')
            return redirect(url_for('auth.login'))

        if not user.activo:
            flash('Esta cuenta de usuario ha sido desactivada.', 'warning')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        user.ultimo_login = datetime.utcnow() # Actualizar fecha de último login
        db.session.commit()
        flash(f'Bienvenido de nuevo, {user.nombre_completo}!', 'success')

        next_page = request.args.get('next')
        # Protección contra Open Redirect: asegurarse que next_page sea una ruta relativa
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index') # Redirigir a la página principal o a un dashboard
        return redirect(next_page)

    return render_template('auth/login.html', title='Iniciar Sesión', form=form)

@bp.route('/logout')
@login_required # Asegurarse que solo usuarios logueados puedan desloguearse
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('index'))

# Podríamos añadir rutas para registro, reseteo de contraseña, etc. aquí en el futuro.