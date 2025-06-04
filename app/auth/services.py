from app import db
from app.models import Usuario
from datetime import datetime

def obtener_usuario_por_username(username):
    """Obtiene un usuario por su nombre de usuario."""
    # Usamos .upper() aquí también para consistencia con cómo se guarda si aplica,
    # pero el modelo Usuario no parece guardar el username en mayúsculas.
    # Si el username se guarda tal cual, no es necesario .upper().
    # Asumiendo que username es sensible a mayúsculas/minúsculas por ahora.
    return Usuario.query.filter_by(username=username).first()

def actualizar_ultimo_login(usuario):
    """Actualiza la fecha y hora del último login de un usuario."""
    usuario.ultimo_login = datetime.utcnow()
    # La transacción (add/commit/rollback) se manejará en la capa superior (rutas)
    # db.session.add(usuario) # No es necesario add si el objeto ya está en la sesión
    return usuario

# Puedes añadir más funciones de servicio aquí si implementas registro,
# reseteo de contraseña, etc., que involucren interacción con la BD.