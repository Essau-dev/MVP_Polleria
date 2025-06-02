from datetime import datetime
from app import db, login # Importamos la instancia db y login creada en app/__init__.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # Importar UserMixin
from sqlalchemy import CheckConstraint, UniqueConstraint # Importar para constraints

# --- Modelos de Autenticación y Usuarios (existentes) ---
# Flask-Login requiere una función 'user_loader'
@login.user_loader
def load_user(id):
    # Flask-Login pasa el ID como string, convertir a int
    # Usar db.session.get para SQLAlchemy 2.x (recomendado)
    return db.session.get(Usuario, int(id))

# Si integramos Flask-Login, Usuario debería heredar de UserMixin
class Usuario(UserMixin, db.Model): # Añadir UserMixin
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    nombre_completo = db.Column(db.String(150), nullable=False)
    rol = db.Column(db.String(30), nullable=False, index=True) # Ej: 'ADMINISTRADOR', 'CAJERO'
    activo = db.Column(db.Boolean, nullable=False, default=True, index=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ultimo_login = db.Column(db.DateTime, nullable=True)

    # Relaciones (se añadirán a medida que definamos otros modelos)
    # pedidos_registrados = db.relationship('Pedido', foreign_keys='Pedido.usuario_id', back_populates='usuario_creador', lazy='dynamic')
    # pedidos_asignados_repartidor = db.relationship('Pedido', foreign_keys='Pedido.repartidor_id', back_populates='repartidor_asignado', lazy='dynamic')
    # movimientos_caja_registrados = db.relationship('MovimientoCaja', back_populates='usuario_responsable', lazy='dynamic')
    # cortes_caja_realizados = db.relationship('CorteCaja', back_populates='usuario_responsable_corte', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.username} ({self.rol})>'

# --- Modelo Cliente (existente) ---
class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), index=True, nullable=False)
    apellidos = db.Column(db.String(150), index=True, nullable=True)
    alias = db.Column(db.String(80), index=True, nullable=True)
    tipo_cliente = db.Column(db.String(50), index=True, nullable=False, default='PUBLICO') # Ej: 'PUBLICO', 'COCINA'
    notas_cliente = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    activo = db.Column(db.Boolean, nullable=False, default=True, index=True)

    # Relaciones
    # telefonos = db.relationship('Telefono', back_populates='cliente', lazy='dynamic', cascade='all, delete-orphan')
    # direcciones = db.relationship('Direccion', back_populates='cliente', lazy='dynamic', cascade='all, delete-orphan')
    # pedidos = db.relationship('Pedido', back_populates='cliente', lazy='dynamic')

    def get_nombre_completo(self):
        if self.apellidos:
            return f"{self.nombre} {self.apellidos}"
        return self.nombre

    def __repr__(self):
        return f'<Cliente {self.id}: {self.get_nombre_completo()}>'

# --- Tablas de Asociación para Modificaciones (Many-to-Many) ---

producto_modificacion_association = db.Table('producto_modificacion_association',
    db.Column('producto_id', db.String(10), db.ForeignKey('productos.id'), primary_key=True),
    db.Column('modificacion_id', db.Integer, db.ForeignKey('modificaciones.id'), primary_key=True)
)

subproducto_modificacion_association = db.Table('subproducto_modificacion_association',
    db.Column('subproducto_id', db.Integer, db.ForeignKey('subproductos.id'), primary_key=True),
    db.Column('modificacion_id', db.Integer, db.ForeignKey('modificaciones.id'), primary_key=True)
)

# --- Modelos de Catálogo de Productos ---

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.String(10), primary_key=True) # Código del producto, ej: 'PECH'
    nombre = db.Column(db.String(100), index=True, unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(50), index=True, nullable=False) # Ej: 'POLLO_CRUDO', 'MENUDENCIA'
    activo = db.Column(db.Boolean, nullable=False, default=True, index=True)

    # Relaciones
    subproductos = db.relationship('Subproducto', back_populates='producto_padre', lazy='dynamic', cascade='all, delete-orphan')
    modificaciones_directas = db.relationship(
        'Modificacion',
        secondary=producto_modificacion_association,
        back_populates='productos_asociados',
        lazy='dynamic'
    )
    precios = db.relationship('Precio', foreign_keys='Precio.producto_id', back_populates='producto_base', lazy='dynamic', cascade='all, delete-orphan')
    # items_pedido = db.relationship('PedidoItem', foreign_keys='PedidoItem.producto_id', back_populates='producto', lazy='dynamic') # Se añadirá con PedidoItem


    def __repr__(self):
        return f'<Producto {self.id}: {self.nombre}>'

class Subproducto(db.Model):
    __tablename__ = 'subproductos'

    id = db.Column(db.Integer, primary_key=True)
    producto_padre_id = db.Column(db.String(10), db.ForeignKey('productos.id'), nullable=False, index=True)
    codigo_subprod = db.Column(db.String(15), unique=True, nullable=False, index=True) # Ej: 'PP', 'PG'
    nombre = db.Column(db.String(100), nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=True) # Corrected line
    activo = db.Column(db.Boolean, nullable=False, default=True, index=True)

    # Relaciones
    producto_padre = db.relationship('Producto', back_populates='subproductos')
    modificaciones_aplicables = db.relationship(
        'Modificacion',
        secondary=subproducto_modificacion_association,
        back_populates='subproductos_asociados',
        lazy='dynamic'
    )
    precios = db.relationship('Precio', foreign_keys='Precio.subproducto_id', back_populates='subproducto_base', lazy='dynamic', cascade='all, delete-orphan')
    # items_pedido = db.relationship('PedidoItem', foreign_keys='PedidoItem.subproducto_id', back_populates='subproducto', lazy='dynamic') # Se añadirá con PedidoItem

    def __repr__(self):
        return f'<Subproducto {self.codigo_subprod}: {self.nombre} (Padre: {self.producto_padre_id})>'

class Modificacion(db.Model):
    __tablename__ = 'modificaciones'

    id = db.Column(db.Integer, primary_key=True)
    codigo_modif = db.Column(db.String(20), unique=True, nullable=False, index=True) # Ej: 'MOLI', 'ASAR'
    nombre = db.Column(db.String(100), nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True, index=True)

    # Relaciones
    productos_asociados = db.relationship(
        'Producto',
        secondary=producto_modificacion_association,
        back_populates='modificaciones_directas',
        lazy='dynamic'
    )
    subproductos_asociados = db.relationship(
        'Subproducto',
        secondary=subproducto_modificacion_association,
        back_populates='modificaciones_aplicables',
        lazy='dynamic'
    )
    # items_pedido = db.relationship('PedidoItem', back_populates='modificacion_aplicada', lazy='dynamic') # Se añadirá con PedidoItem


    def __repr__(self):
        return f'<Modificacion {self.codigo_modif}: {self.nombre}>'

class Precio(db.Model):
    __tablename__ = 'precios'

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.String(10), db.ForeignKey('productos.id'), nullable=True, index=True)
    subproducto_id = db.Column(db.Integer, db.ForeignKey('subproductos.id'), nullable=True, index=True)
    tipo_cliente = db.Column(db.String(50), nullable=False, index=True) # Ej: 'PUBLICO', 'COCINA'
    precio_kg = db.Column(db.Float, nullable=False)
    cantidad_minima_kg = db.Column(db.Float, nullable=False, default=0.0)
    etiqueta_promo = db.Column(db.String(100), nullable=True)
    fecha_inicio_vigencia = db.Column(db.Date, nullable=True, index=True)
    fecha_fin_vigencia = db.Column(db.Date, nullable=True, index=True)
    activo = db.Column(db.Boolean, nullable=False, default=True, index=True)

    # Relaciones
    producto_base = db.relationship('Producto', foreign_keys=[producto_id], back_populates='precios')
    subproducto_base = db.relationship('Subproducto', foreign_keys=[subproducto_id], back_populates='precios')

    # Constraints
    __table_args__ = (
        CheckConstraint(
            '(producto_id IS NOT NULL AND subproducto_id IS NULL) OR (producto_id IS NULL AND subproducto_id IS NOT NULL)',
            name='chk_precio_target_not_both_or_none' # Nombre ajustado para claridad
        ),
        UniqueConstraint('producto_id', 'tipo_cliente', 'cantidad_minima_kg', name='uq_precio_prod_tipo_cantmin'),
        UniqueConstraint('subproducto_id', 'tipo_cliente', 'cantidad_minima_kg', name='uq_precio_subprod_tipo_cantmin'),
    )

    def __repr__(self):
        target = f"Prod:{self.producto_id}" if self.producto_id else f"SubP:{self.subproducto_id}"
        return f'<Precio {self.id} ({target}) Cliente:{self.tipo_cliente} ${self.precio_kg}>'

# --- Otros modelos que se definirán más adelante ---
# Telefono, Direccion, Pedido, PedidoItem, ProductoAdicional, MovimientoCaja, MovimientoDenominacion, CorteCaja, DenominacionCorteCaja, ConfiguracionSistema