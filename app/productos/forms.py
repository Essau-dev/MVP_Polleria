from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from app.models import Producto, Subproducto # Añadir Subproducto para validación
from app.models import Modificacion # ¡Asegúrate de importar Modificacion!

# Lista de categorías predefinidas (podría venir de la BD o config en el futuro)
CATEGORIAS_PRODUCTO = [
    ('Producto', 'Producto'),
    ('Subproducto', 'Subproducto'),
    ('Especial', 'Especial'), # Ejemplo de otra categoría
    ('Corte', 'Corte')
]

class ProductoForm(FlaskForm):
    id = StringField(
        'Código del Producto (ID)',
        validators=[
            DataRequired(message="El código del producto es obligatorio."),
            Length(min=1, max=10, message="El código debe tener entre 1 y 10 caracteres.")
        ],
        render_kw={"placeholder": "Ej: PECH, AL, SRT"}
    )
    nombre = StringField(
        'Nombre del Producto',
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=100)
        ],
        render_kw={"placeholder": "Ej: Pechuga de Pollo"}
    )
    descripcion = TextAreaField(
        'Descripción',
        validators=[Optional(), Length(max=500)],
        render_kw={"rows": 3, "placeholder": "Descripción detallada del producto (opcional)"}
    )
    categoria = SelectField(
        'Categoría',
        choices=CATEGORIAS_PRODUCTO,
        validators=[DataRequired(message="Selecciona una categoría.")]
    )
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar Producto')

    def __init__(self, original_producto_id=None, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.original_producto_id = original_producto_id

    def validate_id(self, id_field):
        if self.original_producto_id is None or self.original_producto_id != id_field.data:
            producto_existente = Producto.query.filter_by(id=id_field.data.upper()).first() # Convertir a mayúsculas para la búsqueda
            if producto_existente:
                raise ValidationError('Este código de producto ya existe. Por favor, elige otro.')

# --- Nuevo Formulario para Subproductos ---
class SubproductoForm(FlaskForm):
    # No incluimos producto_padre_id aquí, se pasará en la ruta
    codigo_subprod = StringField(
        'Código del Subproducto',
        validators=[
            DataRequired(message="El código del subproducto es obligatorio."),
            Length(min=1, max=15, message="El código debe tener entre 1 y 15 caracteres.")
        ],
        render_kw={"placeholder": "Ej: PP, PG, CD"}
    )
    nombre = StringField(
        'Nombre del Subproducto',
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=100)
        ],
        render_kw={"placeholder": "Ej: Pulpa de Pechuga"}
    )
    descripcion = TextAreaField(
        'Descripción del Subproducto',
        validators=[Optional(), Length(max=500)],
        render_kw={"rows": 3, "placeholder": "Descripción detallada (opcional)"}
    )
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar Subproducto')

    def __init__(self, original_codigo_subprod=None, *args, **kwargs):
        super(SubproductoForm, self).__init__(*args, **kwargs)
        self.original_codigo_subprod = original_codigo_subprod

    def validate_codigo_subprod(self, codigo_field):
        # Si estamos creando (original_codigo_subprod es None) o
        # si el código ha cambiado respecto al original
        if self.original_codigo_subprod is None or self.original_codigo_subprod != codigo_field.data:
            subproducto_existente = Subproducto.query.filter_by(codigo_subprod=codigo_field.data.upper()).first() # Convertir a mayúsculas para la búsqueda
            if subproducto_existente:
                raise ValidationError('Este código de subproducto ya existe. Por favor, elige otro.')

# --- Nuevo Formulario para Modificaciones ---
class ModificacionForm(FlaskForm):
    codigo_modif = StringField(
        'Código de la Modificación',
        validators=[
            DataRequired(message="El código es obligatorio."),
            Length(min=1, max=20)
        ],
        render_kw={"placeholder": "Ej: MOLI, ASAR_PECH"}
    )
    nombre = StringField(
        'Nombre de la Modificación',
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=100)
        ],
        render_kw={"placeholder": "Ej: Molida, Para Asar (Pechuga)"}
    )
    descripcion = TextAreaField(
        'Descripción (Opcional)',
        validators=[Optional(), Length(max=500)],
        render_kw={"rows": 3}
    )
    activo = BooleanField('Activa', default=True)
    submit = SubmitField('Guardar Modificación')

    def __init__(self, original_codigo_modif=None, *args, **kwargs):
        super(ModificacionForm, self).__init__(*args, **kwargs)
        self.original_codigo_modif = original_codigo_modif

    def validate_codigo_modif(self, codigo_field):
        if self.original_codigo_modif is None or self.original_codigo_modif != codigo_field.data:
            modificacion_existente = Modificacion.query.filter_by(codigo_modif=codigo_field.data).first()
            if modificacion_existente:
                raise ValidationError('Este código de modificación ya existe. Por favor, elige otro.')