from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[DataRequired(message="El nombre de usuario es obligatorio."),
                    Length(min=3, max=80, message="El usuario debe tener entre 3 y 80 caracteres.")],
        render_kw={"placeholder": "Nombre de usuario"}
    )
    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message="La contraseña es obligatoria.")],
        render_kw={"placeholder": "Contraseña"}
    )
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')