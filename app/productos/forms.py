from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from app.models import Producto # Para validación de ID único

# Lista de categorías predefinidas (podría venir de la BD o config en el futuro)
CATEGORIAS_PRODUCTO = [
    ('Producto', 'Producto'),
    ('Subproducto', 'Subproducto'),
    ('Especial', 'Especial'),
    ('Corte', 'Corte'), # Ejemplo de otra categoría
    ('Otro', 'Otro')
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

    # Validación personalizada para asegurar que el ID (código) del producto sea único al crear
    # y que no se cambie a uno existente al editar (si el ID es editable y no es el original).
    def __init__(self, original_producto_id=None, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.original_producto_id = original_producto_id

    def validate_id(self, id_field):
        # Si estamos creando (original_producto_id es None) o
        # si el ID ha cambiado respecto al original
        if self.original_producto_id is None or self.original_producto_id != id_field.data:
            producto_existente = Producto.query.filter_by(id=id_field.data).first()
            if producto_existente:
                raise ValidationError('Este código de producto ya existe. Por favor, elige otro.')