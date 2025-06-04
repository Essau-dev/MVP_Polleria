from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app import db
from app.productos import bp
from app.models import Producto, Subproducto, Modificacion, Precio # Importar modelos si aún se necesitan para tipos o relaciones directas
from app.productos.forms import ProductoForm, SubproductoForm, ModificacionForm # Importar los formularios
from app.productos import services # Importar el módulo de servicios

# --- Rutas para Productos Principales ---

# Ruta para LISTAR productos
@bp.route('/')
@login_required
def listar_productos():
    if current_user.rol != 'ADMINISTRADOR':
        flash('No tienes permiso para acceder a esta sección.', 'danger')
        return redirect(url_for('index'))

    # Usar la función de servicio para obtener los productos
    productos_list = services.obtener_todos_los_productos()

    return render_template('productos/listar_productos.html',
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
        try:
            # Usar la función de servicio para crear el producto
            services.crear_producto(form.data)
            db.session.commit() # Confirmar la transacción
            flash(f'Producto "{form.nombre.data}" creado exitosamente.', 'success')
            return redirect(url_for('productos.listar_productos'))
        except Exception as e:
            db.session.rollback() # Revertir la transacción en caso de error
            flash(f'Error al crear el producto: {e}', 'danger')

    return render_template('productos/crear_editar_producto.html',
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

    # Usar la función de servicio para obtener el producto
    producto_a_editar = services.obtener_producto_por_id(producto_id)
    if not producto_a_editar:
        flash(f'Producto con ID "{producto_id}" no encontrado.', 'warning')
        return redirect(url_for('productos.listar_productos'))

    # Pasamos el ID original para la validación en el formulario
    # obj=producto_a_editar precarga los datos del producto en el formulario para GET
    form = ProductoForm(original_producto_id=producto_a_editar.id, obj=producto_a_editar)

    if form.validate_on_submit():
        try:
            # Usar la función de servicio para actualizar el producto
            services.actualizar_producto(producto_a_editar, form.data)
            db.session.commit() # Confirmar la transacción
            flash(f'Producto "{producto_a_editar.nombre}" actualizado exitosamente.', 'success')
            return redirect(url_for('productos.listar_productos'))
        except Exception as e:
            db.session.rollback() # Revertir la transacción en caso de error
            flash(f'Error al actualizar el producto: {e}', 'danger')

    # Para GET, el formulario se poblará con obj=producto_a_editar
    return render_template('productos/crear_editar_producto.html',
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

    # Usar la función de servicio para obtener el producto
    producto = services.obtener_producto_por_id(producto_id)
    if not producto:
        flash(f'Producto con ID "{producto_id}" no encontrado.', 'warning')
        return redirect(url_for('productos.listar_productos'))

    # Usar funciones de servicio para obtener las relaciones
    modificaciones_directas = services.obtener_modificaciones_para_producto(producto) # Asumiendo que agregamos esta función al servicio
    subproductos_asociados = services.obtener_subproductos_para_producto(producto)
    precios_del_producto = services.obtener_precios_para_producto(producto)

    return render_template('productos/ver_producto.html',
                           title=f"Detalle: {producto.nombre}",
                           producto=producto,
                           modificaciones=modificaciones_directas,
                           subproductos=subproductos_asociados,
                           precios=precios_del_producto)

# --- Rutas para Subproductos ---

@bp.route('/<string:producto_padre_id>/subproducto/crear', methods=['GET', 'POST'])
@login_required
def crear_subproducto(producto_padre_id):
    if current_user.rol != 'ADMINISTRADOR':
        flash('No tienes permiso para crear subproductos.', 'danger')
        return redirect(url_for('productos.listar_productos'))

    # Usar la función de servicio para obtener el producto padre
    producto_padre = services.obtener_producto_por_id(producto_padre_id)
    if not producto_padre:
        flash(f'Producto padre con ID "{producto_padre_id}" no encontrado.', 'warning')
        return redirect(url_for('productos.listar_productos'))

    form = SubproductoForm() # No pasamos original_codigo_subprod porque es nuevo
    if form.validate_on_submit():
        try:
            # Usar la función de servicio para crear el subproducto
            services.crear_subproducto(producto_padre, form.data)
            db.session.commit() # Confirmar la transacción
            flash(f'Subproducto "{form.nombre.data}" creado y asociado a "{producto_padre.nombre}".', 'success')
            return redirect(url_for('productos.ver_producto', producto_id=producto_padre.id))
        except Exception as e:
            db.session.rollback() # Revertir la transacción en caso de error
            flash(f'Error al crear el subproducto: {str(e)}', 'danger')

    return render_template('productos/crear_editar_subproducto.html',
                           title=f"Crear Subproducto para: {producto_padre.nombre}",
                           form=form,
                           producto_padre=producto_padre,
                           es_editar=False)

@bp.route('/subproducto/editar/<int:subproducto_id>', methods=['GET', 'POST'])
@login_required
def editar_subproducto(subproducto_id):
    if current_user.rol != 'ADMINISTRADOR':
        flash('No tienes permiso para editar subproductos.', 'danger')
        return redirect(url_for('productos.listar_productos'))

    # Usar la función de servicio para obtener el subproducto
    subproducto_a_editar = services.obtener_subproducto_por_id(subproducto_id)
    if not subproducto_a_editar:
        flash(f'Subproducto con ID "{subproducto_id}" no encontrado.', 'warning')
        return redirect(url_for('productos.listar_productos')) # O a la vista del producto padre si se tiene

    producto_padre = subproducto_a_editar.producto_padre # Acceder al producto padre (la relación ya está cargada)

    form = SubproductoForm(original_codigo_subprod=subproducto_a_editar.codigo_subprod, obj=subproducto_a_editar)

    if form.validate_on_submit():
        try:
            # Usar la función de servicio para actualizar el subproducto
            services.actualizar_subproducto(subproducto_a_editar, form.data)
            db.session.commit() # Confirmar la transacción
            flash(f'Subproducto "{subproducto_a_editar.nombre}" actualizado.', 'success')
            return redirect(url_for('productos.ver_producto', producto_id=producto_padre.id))
        except Exception as e:
            db.session.rollback() # Revertir la transacción en caso de error
            flash(f'Error al actualizar el subproducto: {str(e)}', 'danger')

    return render_template('productos/crear_editar_subproducto.html',
                           title=f"Editar Subproducto: {subproducto_a_editar.nombre}",
                           form=form,
                           producto_padre=producto_padre, # Para mostrar contexto
                           subproducto=subproducto_a_editar, # Para referencia en la plantilla si es necesario
                           es_editar=True)

# --- Rutas para Modificaciones ---

@bp.route('/modificaciones')
@login_required
def listar_modificaciones():
    if current_user.rol != 'ADMINISTRADOR':
        flash('No tienes permiso para acceder a esta sección.', 'danger')
        return redirect(url_for('index')) # O a productos.listar_productos

    # Usar la función de servicio para obtener las modificaciones
    modificaciones_list = services.obtener_todas_las_modificaciones()

    return render_template('productos/listar_modificaciones.html',
                           modificaciones=modificaciones_list,
                           title="Gestión de Modificaciones")

@bp.route('/modificacion/crear', methods=['GET', 'POST'])
@login_required
def crear_modificacion():
    if current_user.rol != 'ADMINISTRADOR':
        flash('No tienes permiso para crear modificaciones.', 'danger')
        return redirect(url_for('productos.listar_modificaciones'))

    form = ModificacionForm()
    if form.validate_on_submit():
        try:
            # Usar la función de servicio para crear la modificación
            services.crear_modificacion(form.data)
            db.session.commit() # Confirmar la transacción
            flash(f'Modificación "{form.nombre.data}" creada exitosamente.', 'success')
            return redirect(url_for('productos.listar_modificaciones'))
        except Exception as e:
            db.session.rollback() # Revertir la transacción en caso de error
            flash(f'Error al crear la modificación: {str(e)}', 'danger')

    return render_template('productos/crear_editar_modificaciones.html',
                           title="Crear Nueva Modificación",
                           form=form,
                           es_editar=False)

@bp.route('/modificacion/editar/<int:modificacion_id>', methods=['GET', 'POST'])
@login_required
def editar_modificacion(modificacion_id):
    if current_user.rol != 'ADMINISTRADOR':
        flash('No tienes permiso para editar modificaciones.', 'danger')
        return redirect(url_for('productos.listar_modificaciones'))

    # Usar la función de servicio para obtener la modificación
    modificacion_a_editar = services.obtener_modificacion_por_id(modificacion_id)
    if not modificacion_a_editar:
        flash(f'Modificación con ID "{modificacion_id}" no encontrada.', 'warning')
        return redirect(url_for('productos.listar_modificaciones'))

    form = ModificacionForm(original_codigo_modif=modificacion_a_editar.codigo_modif, obj=modificacion_a_editar)

    if form.validate_on_submit():
        try:
            # Usar la función de servicio para actualizar la modificación
            services.actualizar_modificacion(modificacion_a_editar, form.data)
            db.session.commit() # Confirmar la transacción
            flash(f'Modificación "{modificacion_a_editar.nombre}" actualizada exitosamente.', 'success')
            return redirect(url_for('productos.listar_modificaciones'))
        except Exception as e:
            db.session.rollback() # Revertir la transacción en caso de error
            flash(f'Error al actualizar la modificación: {str(e)}', 'danger')

    return render_template('productos/crear_editar_modificaciones.html',
                           title=f"Editar Modificación: {modificacion_a_editar.nombre}",
                           form=form,
                           es_editar=True)

# Nota: Las rutas para eliminar productos, subproductos o modificaciones
# seguirían un patrón similar, llamando a funciones de servicio como
# services.eliminar_producto(producto_id), services.eliminar_subproducto(subproducto_id),
# services.eliminar_modificacion(modificacion_id) y manejando el commit/rollback aquí.