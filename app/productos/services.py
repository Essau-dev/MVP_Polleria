from app import db
from app.models import Producto, Subproducto, Modificacion, Precio

# --- Servicios para Productos ---

def obtener_todos_los_productos():
    """Obtiene todos los productos ordenados por nombre."""
    return Producto.query.order_by(Producto.nombre.asc()).all()

def obtener_producto_por_id(producto_id):
    """Obtiene un producto por su ID."""
    # Usamos .upper() aquí también para consistencia con cómo se guarda
    return db.session.get(Producto, producto_id.upper())

def crear_producto(data):
    """Crea un nuevo producto."""
    nuevo_producto = Producto(
        id=data['id'].upper(), # Guardar ID en mayúsculas
        nombre=data['nombre'],
        descripcion=data.get('descripcion'), # Usar .get para campos opcionales
        categoria=data['categoria'],
        activo=data.get('activo', True) # Default a True si no se especifica
    )
    db.session.add(nuevo_producto)
    # La transacción (commit/rollback) se manejará en la capa superior (rutas o comandos CLI)
    return nuevo_producto

def actualizar_producto(producto, data):
    """Actualiza un producto existente."""
    # No actualizamos el ID aquí, asumimos que no cambia post-creación
    producto.nombre = data['nombre']
    producto.descripcion = data.get('descripcion')
    producto.categoria = data['categoria']
    producto.activo = data.get('activo', True)
    # La transacción (commit/rollback) se manejará en la capa superior
    return producto

# --- Servicios para Subproductos ---

def obtener_subproductos_para_producto(producto):
    """Obtiene los subproductos asociados a un producto padre, ordenados por nombre."""
    # Asumimos que la relación 'subproductos' en el modelo Producto es lazy='dynamic' o similar
    return producto.subproductos.order_by(Subproducto.nombre.asc()).all()

def obtener_subproducto_por_id(subproducto_id):
    """Obtiene un subproducto por su ID."""
    return db.session.get(Subproducto, subproducto_id)

def crear_subproducto(producto_padre, data):
    """Crea un nuevo subproducto asociado a un producto padre."""
    nuevo_subproducto = Subproducto(
        producto_padre_id=producto_padre.id,
        codigo_subprod=data['codigo_subprod'].upper(), # Guardar en mayúsculas
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        activo=data.get('activo', True)
    )
    db.session.add(nuevo_subproducto)
    # La transacción se maneja externamente
    return nuevo_subproducto

def actualizar_subproducto(subproducto, data):
    """Actualiza un subproducto existente."""
    # No actualizamos el codigo_subprod aquí si es la PK string
    subproducto.nombre = data['nombre']
    subproducto.descripcion = data.get('descripcion')
    subproducto.activo = data.get('activo', True)
    # La transacción se maneja externamente
    return subproducto

# --- Servicios para Modificaciones ---

def obtener_todas_las_modificaciones():
    """Obtiene todas las modificaciones ordenadas por nombre."""
    return Modificacion.query.order_by(Modificacion.nombre.asc()).all()

def obtener_modificacion_por_id(modificacion_id):
    """Obtiene una modificación por su ID (entero)."""
    return db.session.get(Modificacion, modificacion_id)

def crear_modificacion(data):
    """Crea una nueva modificación."""
    nueva_modificacion = Modificacion(
        codigo_modif=data['codigo_modif'].upper(), # Guardar en mayúsculas
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        activo=data.get('activo', True)
    )
    db.session.add(nueva_modificacion)
    # La transacción se maneja externamente
    return nueva_modificacion

def actualizar_modificacion(modificacion, data):
    """Actualiza una modificación existente."""
    # No actualizamos el codigo_modif aquí si es la PK string
    modificacion.nombre = data['nombre']
    modificacion.descripcion = data.get('descripcion')
    modificacion.activo = data.get('activo', True)
    # La transacción se maneja externamente
    return modificacion

def obtener_modificaciones_para_producto(producto):
    """Obtiene las modificaciones asociadas directamente a un producto, ordenadas por nombre."""
    # Accede a la relación 'modificaciones_directas' definida en el modelo Producto
    # Como la relación es lazy='dynamic', .all() ejecuta la consulta
    return producto.modificaciones_directas.order_by(Modificacion.nombre.asc()).all()

def obtener_modificaciones_para_subproducto(subproducto):
    """Obtiene las modificaciones aplicables a un subproducto, ordenadas por nombre."""
    # Accede a la relación 'modificaciones_aplicables' definida en el modelo Subproducto
    return subproducto.modificaciones_aplicables.order_by(Modificacion.nombre.asc()).all()

# --- Servicios para Precios (Ejemplo) ---

def obtener_precios_para_producto(producto):
    """Obtiene los precios asociados a un producto, ordenados por tipo de cliente y cantidad mínima."""
    # Asumimos que la relación 'precios' en el modelo Producto es lazy='dynamic' o similar
    return producto.precios.order_by(Precio.tipo_cliente.asc(), Precio.cantidad_minima_kg.asc()).all()

# Puedes añadir más funciones de servicio según necesites (ej. para eliminar, buscar, etc.)