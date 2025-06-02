from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app import db
from app.productos import bp
from app.models import Producto, Subproducto, Modificacion, Precio # Importar Subproducto, Modificacion, Precio
from app.productos.forms import ProductoForm # Importar el formulario

# --- Rutas para Productos Principales ---

# Ruta para LISTAR productos (ya existente)
@bp.route('/')
@login_required
def listar_productos():
    if current_user.rol != 'ADMINISTRADOR':
        flash('No tienes permiso para acceder a esta sección.', 'danger')
        return redirect(url_for('index'))
    productos_list = Producto.query.order_by(Producto.nombre.asc()).all()
    # Cambiar 'productos/listar_productos.html' a 'listar_productos.html'
    return render_template('listar_productos.html',
                           productos=productos_list,
                           title="Gestión de Productos")

# Ruta para CREAR un nuevo producto
@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if current_user.rol != 'ADMINISTRADOR':
        flash('No tienes permiso para crear productos.', 'danger')
        return redirect(url_for('productos.listar_productos'))

    form = ProductoForm() # No pasamos original_producto_id porque es nuevo
    if form.validate_on_submit():
        nuevo_producto = Producto(
            id=form.id.data.upper(), # Guardar ID en mayúsculas por consistencia
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            categoria=form.categoria.data,
            activo=form.activo.data
        )
        db.session.add(nuevo_producto)
        try:
            db.session.commit()
            flash(f'Producto "{nuevo_producto.nombre}" creado exitosamente.', 'success')
            return redirect(url_for('productos.listar_productos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el producto: {e}', 'danger')

    return render_template('crear_editar_producto.html', # Usar la plantilla dentro del template_folder del Blueprint
                           title="Crear Nuevo Producto",
                           form=form,
                           es_editar=False)

# Ruta para EDITAR un producto existente
@bp.route('/editar/<string:producto_id>', methods=['GET', 'POST'])
@login_required
def editar_producto(producto_id):
    if current_user.rol != 'ADMINISTRADOR':
        flash('No tienes permiso para editar productos.', 'danger')
        return redirect(url_for('productos.listar_productos'))

    producto_a_editar = db.session.get(Producto, producto_id) # Usar db.session.get
    if not producto_a_editar:
        flash(f'Producto con ID "{producto_id}" no encontrado.', 'warning')
        return redirect(url_for('productos.listar_productos'))

    # Pasamos el ID original para la validación en el formulario
    # obj=producto_a_editar precarga los datos del producto en el formulario para GET
    form = ProductoForm(original_producto_id=producto_a_editar.id, obj=producto_a_editar)

    if form.validate_on_submit():
        # El campo ID no se edita directamente en este formulario para evitar cambiar la PK fácilmente.
        # Si se quisiera permitir editar el ID, se necesitaría una lógica más compleja
        # para manejar las relaciones y asegurar la integridad.
        # Por ahora, asumimos que el ID (código) no cambia una vez creado,
        # o si cambia, la validación del form ya se encargó de la unicidad.
        # Si el campo ID del formulario es diferente al producto_a_editar.id original Y ES EL MISMO CAMPO EN EL FORM,
        # la validación de unicidad en el form ya lo habrá chequeado.
        # Si el ID *NO* debe ser editable en el formulario, deshabilítalo en la plantilla o no lo incluyas para edición.

        # Actualizar los campos del producto con los datos del formulario
        # form.populate_obj(producto_a_editar) # Alternativa a la asignación manual
        producto_a_editar.nombre = form.nombre.data
        producto_a_editar.descripcion = form.descripcion.data
        producto_a_editar.categoria = form.categoria.data
        producto_a_editar.activo = form.activo.data
        # Si permites que el ID del producto se modifique a través del formulario:
        # producto_a_editar.id = form.id.data.upper() # ¡Cuidado con cambiar PKs!

        try:
            db.session.commit()
            flash(f'Producto "{producto_a_editar.nombre}" actualizado exitosamente.', 'success')
            return redirect(url_for('productos.listar_productos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el producto: {e}', 'danger')

    # Para GET, el formulario se poblará con obj=producto_a_editar
    # Si el campo ID se muestra en el form de edición, se mostrará el actual.
    return render_template('crear_editar_producto.html', # Usar la plantilla dentro del template_folder del Blueprint
                           title=f"Editar Producto: {producto_a_editar.nombre}",
                           form=form,
                           producto=producto_a_editar, # Pasamos el producto para referencia en la plantilla
                           es_editar=True)

# Ruta para VER detalles de un producto
@bp.route('/ver/<string:producto_id>')
@login_required
def ver_producto(producto_id):
    if current_user.rol != 'ADMINISTRADOR': # O el rol que deba tener acceso a ver detalles
        flash('No tienes permiso para ver los detalles de este producto.', 'danger')
        return redirect(url_for('productos.listar_productos'))

    producto = db.session.get(Producto, producto_id.upper())
    if not producto:
        flash(f'Producto con ID "{producto_id}" no encontrado.', 'warning')
        return redirect(url_for('productos.listar_productos'))

    # Aquí, más adelante, también consultaremos subproductos, modificaciones aplicables, y precios.
    # Por ahora, nos enfocamos en los datos directos del producto y lo que ya tenemos relacionado.

    # Para mostrar las modificaciones directas que ya relacionamos:
    # Si la relación es lazy='dynamic', necesitas .all()
    modificaciones_directas = producto.modificaciones_directas.all()

    # Para mostrar los subproductos directos:
    # Si la relación es lazy='dynamic', necesitas .all()
    subproductos_asociados = producto.subproductos.order_by(Subproducto.nombre.asc()).all()

    # Para mostrar los precios directos del producto:
    # Si la relación es lazy='dynamic', necesitas .all()
    precios_del_producto = producto.precios.order_by(Precio.tipo_cliente.asc(), Precio.cantidad_minima_kg.asc()).all()


    return render_template('ver_producto.html', # Usar la plantilla dentro del template_folder del Blueprint
                           title=f"Detalle: {producto.nombre}",
                           producto=producto,
                           modificaciones=modificaciones_directas,
                           subproductos=subproductos_asociados,
                           precios=precios_del_producto)