from app import create_app, db
import click
from flask.cli import with_appcontext
from app.models import Producto, Subproducto, Modificacion, Precio, Usuario # Importar Usuario si se necesita para seeding de usuarios

app = create_app()

# --- Funciones de Seeding ---
def clear_data():
    """Elimina datos de las tablas de catálogo para evitar duplicados en reseeding."""
    # El orden es importante por las FKs si usas cascade delete,
    # o elimina en orden inverso a la creación.
    # Para esta implementación, eliminamos precios, luego asociaciones,
    # luego subproductos, luego productos, luego modificaciones.

    # Desactivar temporalmente las restricciones de clave foránea si es necesario para SQLite
    # db.session.execute(text('PRAGMA foreign_keys = OFF;')) # SQLAlchemy 2.x requires text()

    meta = db.metadata
    # Lista de tablas a limpiar en orden inverso de dependencia
    tables_to_clear = [
        'precios',
        'subproducto_modificacion_association',
        'producto_modificacion_association',
        'subproductos',
        'productos',
        'modificaciones',
        # 'usuarios', # Descomentar si quieres limpiar usuarios también (CUIDADO)
        # 'clientes', # Descomentar si quieres limpiar clientes también (CUIDADO)
    ]

    for table_name in tables_to_clear:
        table = meta.tables.get(table_name)
        if table is not None:
            print(f'Limpiando tabla {table.name}...')
            # SQLAlchemy 2.x style delete
            db.session.execute(table.delete())
        else:
            print(f'Advertencia: Tabla {table_name} no encontrada en metadatos.')

    db.session.commit()

    # Reactivar restricciones de clave foránea si se desactivaron
    # db.session.execute(text('PRAGMA foreign_keys = ON;')) # SQLAlchemy 2.x requires text()


def seed_modificaciones_data():
    modificaciones_data = [
        # Genéricas (pueden aplicar a varios)
        {'codigo_modif': 'ENT', 'nombre': 'Entera/o'},
        {'codigo_modif': 'CORT', 'nombre': 'Cortada/o'},
        {'codigo_modif': 'ASAR', 'nombre': 'Para Asar'},
        {'codigo_modif': 'MILA', 'nombre': 'Milanesa'},
        {'codigo_modif': 'CUBOS', 'nombre': 'En Cubos'},
        {'codigo_modif': 'MOLI', 'nombre': 'Molida/o'},
        {'codigo_modif': 'FILE', 'nombre': 'Filetes'},
        {'codigo_modif': 'FREIR', 'nombre': 'Para Freír'},
        {'codigo_modif': 'SINPIEL', 'nombre': 'Sin Piel'},
        {'codigo_modif': 'FAJI', 'nombre': 'Fajitas'},
        {'codigo_modif': 'LIMP', 'nombre': 'Limpia/o'},
        {'codigo_modif': 'SINGRASA', 'nombre': 'Sin Grasa'},

        # Específicas de Pechuga (PECH)
        {'codigo_modif': 'ENT_PECH', 'nombre': 'Entera (Pechuga)'},
        {'codigo_modif': 'CORT2_PECH', 'nombre': 'Cortada en 2 (Pechuga)'},
        {'codigo_modif': 'CORT3_PECH', 'nombre': 'Cortada en 3 (Pechuga)'},
        {'codigo_modif': 'CORT4_PECH', 'nombre': 'Cortada en 4 (Pechuga)'},
        {'codigo_modif': 'CORT6_PECH', 'nombre': 'Cortada en 6 (Pechuga)'},
        {'codigo_modif': 'ASAR_PECH', 'nombre': 'Para Asar (Pechuga)'},
        {'codigo_modif': 'FREIR_PECH', 'nombre': 'Para Freír (Pechuga)'},
        {'codigo_modif': 'MILA_PECH', 'nombre': 'Milanesa (Pechuga)'},
        {'codigo_modif': 'FAJI_PECH', 'nombre': 'Fajitas (Pechuga)'},
        {'codigo_modif': 'CUBOS_PECH', 'nombre': 'En Cubos (Pechuga)'},
        {'codigo_modif': 'MOLI_PECH', 'nombre': 'Molida (Pechuga)'},
        {'codigo_modif': 'FILE_PECH', 'nombre': 'Filetes (Pechuga)'},

        # Específicas de Pulpa de Pechuga (PP)
        {'codigo_modif': 'ASAR_PP', 'nombre': 'Para Asar (Pulpa Pechuga)'},
        {'codigo_modif': 'MILA_PP', 'nombre': 'Milanesa (Pulpa Pechuga)'},
        {'codigo_modif': 'CUBOS_PP', 'nombre': 'En Cubos (Pulpa Pechuga)'},
        {'codigo_modif': 'MOLI_PP', 'nombre': 'Molida (Pulpa Pechuga)'},
        {'codigo_modif': 'FILE_PP', 'nombre': 'Filetes (Pulpa Pechuga)'},
        {'codigo_modif': 'ENT_PP', 'nombre': 'Entera (Pulpa Pechuga)'},

        # Específicas de Alas (AL)
        {'codigo_modif': 'ENT_AL', 'nombre': 'Enteras (Alas)'},
        {'codigo_modif': 'CORT2_AL', 'nombre': 'Cortadas en 2 (Alas)'},
        {'codigo_modif': 'CORT3_AL', 'nombre': 'Cortadas en 3 (Alas)'},

        # Específicas de Cadera (CD)
        {'codigo_modif': 'ENT_CD', 'nombre': 'Entera (Cadera)'},
        {'codigo_modif': 'CORT_CD', 'nombre': 'Cortada (Cadera)'},
        {'codigo_modif': 'SINPIEL_CD', 'nombre': 'Sin Piel (Cadera)'},

        # Específicas de Huacal (HCL)
        {'codigo_modif': 'ENT_HCL', 'nombre': 'Entero (Huacal)'},
        {'codigo_modif': 'CORT_HCL', 'nombre': 'Cortado (Huacal)'},

        # Específicas de Retazo (RTZ)
        {'codigo_modif': 'ENT_RTZ', 'nombre': 'Entero (Retazo)'},
        {'codigo_modif': 'CORT_RTZ', 'nombre': 'Cortado (Retazo)'},
        {'codigo_modif': 'SINPIEL_RTZ', 'nombre': 'Sin Piel (Retazo)'},

        # Específicas de Pierna (PG)
        {'codigo_modif': 'ENT_PG', 'nombre': 'Enteras (Pierna)'},
        {'codigo_modif': 'ASAR_PG', 'nombre': 'Para Asar (Pierna)'},
        {'codigo_modif': 'MILA_PG', 'nombre': 'Milanesa (Pierna)'},
        {'codigo_modif': 'FREIR_PG', 'nombre': 'Para Freír (Pierna)'},
        {'codigo_modif': 'SINPIEL_PG', 'nombre': 'Sin Piel (Pierna)'},

        # Específicas de Muslo (MSL)
        {'codigo_modif': 'ENT_MSL', 'nombre': 'Entero(s) (Muslo)'},
        {'codigo_modif': 'ASAR_MSL', 'nombre': 'Para Asar (Muslo)'},
        {'codigo_modif': 'FREIR_MSL', 'nombre': 'Para Freír (Muslo)'},
        {'codigo_modif': 'MILA_MSL', 'nombre': 'Milanesa (Muslo)'},
        {'codigo_modif': 'SINPIEL_MSL', 'nombre': 'Sin Piel (Muslo)'},

        # Específicas de Pulpa de Perniles (PP-PM)
        {'codigo_modif': 'ASAR_PPPM', 'nombre': 'Para Asar (Pulpa Pernil)'},
        {'codigo_modif': 'MILA_PPPM', 'nombre': 'Milanesa (Pulpa Pernil)'},
        {'codigo_modif': 'FAJI_PPPM', 'nombre': 'Fajitas (Pulpa Pernil)'},
        {'codigo_modif': 'ENT_PPPM', 'nombre': 'Entera (Pulpa Pernil)'},

        # Específicas de Molida de Perniles (M-PM) - ninguna realmente, ya es estado final
        {'codigo_modif': 'NINGUNA_MPM', 'nombre': 'Molida de Pernil (Sin mod. adicional)'},

        # Específicas de Perniles (PM)
        {'codigo_modif': 'ENT_PM', 'nombre': 'Enteros (Perniles Unidos)'},
        {'codigo_modif': 'CORT_PM', 'nombre': 'Cortados (Pierna y Muslo Separados)'},
        {'codigo_modif': 'ASAR_PM', 'nombre': 'Para Asar (Perniles Unidos)'},
        {'codigo_modif': 'MILA_PM', 'nombre': 'Milanesa (Perniles)'},
        {'codigo_modif': 'FREIR_PM', 'nombre': 'Para Freír (Perniles Unidos)'},
        {'codigo_modif': 'SINPIEL_PM', 'nombre': 'Sin Piel (Perniles)'},

        # Específicas de Patas (PT)
        {'codigo_modif': 'LIMP_PT', 'nombre': 'Limpias (Patas)'},
        {'codigo_modif': 'ENT_PT', 'nombre': 'Enteras (Patas)'},

        # Específicas de Molleja (MLJ)
        {'codigo_modif': 'SINGRASA_MLJ', 'nombre': 'Sin Grasa (Molleja)'},
        {'codigo_modif': 'LIMP_MLJ', 'nombre': 'Limpia (Molleja)'},

        # Específicas de Higado (HGD)
        {'codigo_modif': 'LIMP_HGD', 'nombre': 'Limpio (Hígado)'},

        # Específicas de Molleja con Hígado (MHG)
        {'codigo_modif': 'SINGRASA_MHG', 'nombre': 'Sin Grasa (Molleja c/Hígado)'},
        {'codigo_modif': 'LIMP_MHG', 'nombre': 'Limpios (Molleja c/Hígado)'},

        # Específicas de Pollo Surtido (SRT)
        {'codigo_modif': 'CONHCL_SRT', 'nombre': 'Con Huacal (Surtida)'},
        {'codigo_modif': 'CONCD_SRT', 'nombre': 'Con Cadera (Surtida)'},
        {'codigo_modif': 'SINPIEL_SRT', 'nombre': 'Predominantemente Sin Piel (Surtida)'},
        {'codigo_modif': 'PZGRANDE_SRT', 'nombre': 'Piezas Grandes (Surtida)'}, # Ajustado PiezasaGrandes
        {'codigo_modif': 'PZCHICA_SRT', 'nombre': 'Piezas Chicas/Medianas (Surtida)'} # Ajustado PiezasChicas
    ]
    for mod_data in modificaciones_data:
        mod = Modificacion.query.filter_by(codigo_modif=mod_data['codigo_modif']).first()
        if not mod:
            mod = Modificacion(**mod_data)
            db.session.add(mod)
    db.session.commit()
    print("Modificaciones pobladas.")

def seed_productos_subproductos_data():
    productos_data = [
        {'id': 'PECH', 'nombre': 'Pechuga de Pollo', 'categoria': 'Pollo Crudo', 'activo': True,
         'mod_directas_cods': ['ENT_PECH', 'CORT2_PECH', 'CORT3_PECH', 'CORT4_PECH', 'CORT6_PECH', 'ASAR_PECH', 'FREIR_PECH', 'MILA_PECH', 'FAJI_PECH', 'CUBOS_PECH', 'MOLI_PECH', 'FILE_PECH'],
         'subproductos': [
             {'codigo_subprod': 'PP', 'nombre': 'Pulpa de Pechuga', 'activo': True,
              'mod_aplicables_cods': ['ASAR_PP', 'MILA_PP', 'CUBOS_PP', 'MOLI_PP', 'FILE_PP', 'ENT_PP']}
         ]},
        {'id': 'AL', 'nombre': 'Alas de Pollo', 'categoria': 'Pollo Crudo', 'activo': True,
         'mod_directas_cods': ['ENT_AL', 'CORT2_AL', 'CORT3_AL'],
         'subproductos': []},
        {'id': 'RTZ', 'nombre': 'Retazo de Pollo', 'categoria': 'Pollo Crudo', 'activo': True,
         'mod_directas_cods': ['ENT_RTZ', 'CORT_RTZ', 'SINPIEL_RTZ'],
         'subproductos': [
             {'codigo_subprod': 'CD', 'nombre': 'Cadera de Pollo', 'activo': True,
              'mod_aplicables_cods': ['ENT_CD', 'CORT_CD', 'SINPIEL_CD']},
             {'codigo_subprod': 'HCL', 'nombre': 'Huacal de Pollo', 'activo': True,
              'mod_aplicables_cods': ['ENT_HCL', 'CORT_HCL']}
         ]},
        {'id': 'PM', 'nombre': 'Perniles (Pierna y Muslo)', 'categoria': 'Pollo Crudo', 'activo': True,
         'mod_directas_cods': ['ENT_PM', 'CORT_PM', 'ASAR_PM', 'MILA_PM', 'FREIR_PM', 'SINPIEL_PM'],
         'subproductos': [
             {'codigo_subprod': 'PG', 'nombre': 'Pierna de Pollo', 'activo': True,
              'mod_aplicables_cods': ['ENT_PG', 'ASAR_PG', 'MILA_PG', 'FREIR_PG', 'SINPIEL_PG']},
             {'codigo_subprod': 'MSL', 'nombre': 'Muslo de Pollo', 'activo': True,
              'mod_aplicables_cods': ['ENT_MSL', 'ASAR_MSL', 'FREIR_MSL', 'MILA_MSL', 'SINPIEL_MSL']},
             {'codigo_subprod': 'PP-PM', 'nombre': 'Pulpa de Perniles (Pierna y Muslo)', 'activo': True,
              'mod_aplicables_cods': ['ASAR_PPPM', 'MILA_PPPM', 'FAJI_PPPM', 'ENT_PPPM']},
             {'codigo_subprod': 'M-PM', 'nombre': 'Molida de Perniles (Pierna y Muslo)', 'activo': True,
              'mod_aplicables_cods': ['NINGUNA_MPM']}
         ]},
        {'id': 'PT', 'nombre': 'Patas de Pollo', 'categoria': 'Menudencia', 'activo': True,
         'mod_directas_cods': ['LIMP_PT', 'ENT_PT'],
         'subproductos': []},
        {'id': 'MHG', 'nombre': 'Molleja con Hígado (Paquete)', 'categoria': 'Menudencia', 'activo': True,
         'mod_directas_cods': ['SINGRASA_MHG', 'LIMP_MHG'],
         'subproductos': [
             {'codigo_subprod': 'MLJ', 'nombre': 'Molleja de Pollo (Sola)', 'activo': True,
              'mod_aplicables_cods': ['SINGRASA_MLJ', 'LIMP_MLJ']},
             {'codigo_subprod': 'HGD', 'nombre': 'Hígado de Pollo (Solo)', 'activo': True,
              'mod_aplicables_cods': ['LIMP_HGD']}
         ]},
        {'id': 'SRT', 'nombre': 'Pollo Surtido (Piezas Variadas)', 'categoria': 'Pollo Crudo', 'activo': True, 'descripcion': 'Mezcla de diferentes piezas de pollo.',
         'mod_directas_cods': ['CONHCL_SRT', 'CONCD_SRT', 'SINPIEL_SRT', 'PZGRANDE_SRT', 'PZCHICA_SRT'],
         'subproductos': []}
    ]

    for prod_data in productos_data:
        producto = Producto.query.filter_by(id=prod_data['id']).first()
        if not producto:
            producto = Producto(id=prod_data['id'], nombre=prod_data['nombre'], categoria=prod_data['categoria'], activo=prod_data['activo'], descripcion=prod_data.get('descripcion'))
            db.session.add(producto)

        # Asociar modificaciones directas al producto
        for mod_cod in prod_data.get('mod_directas_cods', []):
            mod = Modificacion.query.filter_by(codigo_modif=mod_cod).first()
            if mod: # Asegurarse de que la modificación exista
                 if mod not in producto.modificaciones_directas:
                    producto.modificaciones_directas.append(mod)
            else:
                 print(f"Advertencia: Modificación con código '{mod_cod}' no encontrada para el producto '{producto.id}'.")


        for sub_data in prod_data.get('subproductos', []):
            subproducto = Subproducto.query.filter_by(codigo_subprod=sub_data['codigo_subprod']).first()
            if not subproducto:
                subproducto = Subproducto(
                    producto_padre_id=producto.id,
                    codigo_subprod=sub_data['codigo_subprod'],
                    nombre=sub_data['nombre'],
                    activo=sub_data['activo']
                )
                db.session.add(subproducto)

            # Asociar modificaciones aplicables al subproducto
            for mod_cod_sub in sub_data.get('mod_aplicables_cods', []):
                mod_sub = Modificacion.query.filter_by(codigo_modif=mod_cod_sub).first()
                if mod_sub: # Asegurarse de que la modificación exista
                    if mod_sub not in subproducto.modificaciones_aplicables:
                        subproducto.modificaciones_aplicables.append(mod_sub)
                else:
                    print(f"Advertencia: Modificación con código '{mod_cod_sub}' no encontrada para el subproducto '{subproducto.codigo_subprod}'.")

    db.session.commit()
    print("Productos y subproductos poblados con sus modificaciones.")

def seed_precios_data():
    # Es importante que los subproductos ya existan para obtener sus IDs numéricos
    precios_data = [
        # Precios Pechuga (PECH)
        {'producto_id': 'PECH', 'tipo_cliente': 'PUBLICO', 'precio_kg': 120.00},
        {'producto_id': 'PECH', 'tipo_cliente': 'COCINA', 'precio_kg': 115.00},
        {'producto_id': 'PECH', 'tipo_cliente': 'LEAL', 'precio_kg': 110.00},
        {'producto_id': 'PECH', 'tipo_cliente': 'ALIADO', 'precio_kg': 105.00},
        {'producto_id': 'PECH', 'tipo_cliente': 'MAYOREO', 'precio_kg': 100.00, 'cantidad_minima_kg': 10, 'etiqueta_promo': 'Precio Mayoreo (desde 10kg)'},
        # Precios Pulpa de Pechuga (PP) - requiere subproducto_id
        {'codigo_subprod_ref': 'PP', 'tipo_cliente': 'PUBLICO', 'precio_kg': 185.00},
        {'codigo_subprod_ref': 'PP', 'tipo_cliente': 'COCINA', 'precio_kg': 165.00},
        # Precios Alas (AL)
        {'producto_id': 'AL', 'tipo_cliente': 'PUBLICO', 'precio_kg': 118.00},
        {'producto_id': 'AL', 'tipo_cliente': 'PUBLICO', 'precio_kg': 115.00, 'cantidad_minima_kg': 10, 'etiqueta_promo': 'Paquete Alas 10kg'},
        {'producto_id': 'AL', 'tipo_cliente': 'COCINA', 'precio_kg': 107.00},
        {'producto_id': 'AL', 'tipo_cliente': 'MAYOREO', 'precio_kg': 100.00, 'cantidad_minima_kg': 10, 'etiqueta_promo': 'Precio Mayoreo (desde 10kg)'},
        # Precios Retazo (RTZ)
        {'producto_id': 'RTZ', 'tipo_cliente': 'PUBLICO', 'precio_kg': 40.00},
        {'producto_id': 'RTZ', 'tipo_cliente': 'PUBLICO', 'precio_kg': 25.00, 'cantidad_minima_kg': 2, 'etiqueta_promo': 'Promo Retazo 2kg'},
        {'producto_id': 'RTZ', 'tipo_cliente': 'PUBLICO', 'precio_kg': 20.00, 'cantidad_minima_kg': 3, 'etiqueta_promo': 'Promo Retazo 3kg'},
        # Precios Cadera (CD) - subproducto
        {'codigo_subprod_ref': 'CD', 'tipo_cliente': 'PUBLICO', 'precio_kg': 45.00},
        # Precios Huacal (HCL) - subproducto
        {'codigo_subprod_ref': 'HCL', 'tipo_cliente': 'PUBLICO', 'precio_kg': 25.00},
        # Precios Perniles (PM)
        {'producto_id': 'PM', 'tipo_cliente': 'PUBLICO', 'precio_kg': 85.00},
        {'producto_id': 'PM', 'tipo_cliente': 'PUBLICO', 'precio_kg': 80.00, 'cantidad_minima_kg': 2, 'etiqueta_promo': 'Promo Perniles 2kg'},
        {'producto_id': 'PM', 'tipo_cliente': 'COCINA', 'precio_kg': 70.00},
        # Precios Pierna (PG) - subproducto
        {'codigo_subprod_ref': 'PG', 'tipo_cliente': 'PUBLICO', 'precio_kg': 95.00},
        # Precios Muslo (MSL) - subproducto
        {'codigo_subprod_ref': 'MSL', 'tipo_cliente': 'PUBLICO', 'precio_kg': 85.00},
        # Precios Pulpa de Perniles (PP-PM) - subproducto
        {'codigo_subprod_ref': 'PP-PM', 'tipo_cliente': 'PUBLICO', 'precio_kg': 105.00},
        {'codigo_subprod_ref': 'PP-PM', 'tipo_cliente': 'MAYOREO', 'precio_kg': 95.00, 'cantidad_minima_kg': 5, 'etiqueta_promo': 'Mayoreo Pulpa Pernil (desde 5kg)'},
        # Precios Molida de Perniles (M-PM) - subproducto
        {'codigo_subprod_ref': 'M-PM', 'tipo_cliente': 'PUBLICO', 'precio_kg': 110.00},
        # Precios Patas (PT)
        {'producto_id': 'PT', 'tipo_cliente': 'PUBLICO', 'precio_kg': 65.00},
        {'producto_id': 'PT', 'tipo_cliente': 'PUBLICO', 'precio_kg': 55.00, 'cantidad_minima_kg': 2, 'etiqueta_promo': 'Promo Patas 2kg'},
        # Precios Molleja con Hígado (MHG)
        {'producto_id': 'MHG', 'tipo_cliente': 'PUBLICO', 'precio_kg': 35.00},
        {'producto_id': 'MHG', 'tipo_cliente': 'PUBLICO', 'precio_kg': 25.00, 'cantidad_minima_kg': 2, 'etiqueta_promo': 'Promo Molleja c/Hígado 2kg'},
        # Precios Molleja Sola (MLJ) - subproducto
        {'codigo_subprod_ref': 'MLJ', 'tipo_cliente': 'PUBLICO', 'precio_kg': 65.00},
        # Precios Hígado Solo (HGD) - subproducto
        {'codigo_subprod_ref': 'HGD', 'tipo_cliente': 'PUBLICO', 'precio_kg': 25.00},
        # Precios Pollo Surtido (SRT)
        {'producto_id': 'SRT', 'tipo_cliente': 'PUBLICO', 'precio_kg': 68.00},
        {'producto_id': 'SRT', 'tipo_cliente': 'PUBLICO', 'precio_kg': 65.00, 'cantidad_minima_kg': 2, 'etiqueta_promo': 'Promo Surtida 2kg'},
        {'producto_id': 'SRT', 'tipo_cliente': 'PUBLICO', 'precio_kg': 60.00, 'cantidad_minima_kg': 3, 'etiqueta_promo': 'Promo Surtida 3kg'},
        {'producto_id': 'SRT', 'tipo_cliente': 'COCINA', 'precio_kg': 60.00},
    ]

    for precio_info in precios_data:
        # Crear una copia para no modificar el diccionario original
        precio_data_db = precio_info.copy()

        # Si es un precio para subproducto, obtener el ID del subproducto
        if 'codigo_subprod_ref' in precio_data_db:
            codigo_sub = precio_data_db.pop('codigo_subprod_ref')
            subprod = Subproducto.query.filter_by(codigo_subprod=codigo_sub).first()
            if subprod:
                precio_data_db['subproducto_id'] = subprod.id
            else:
                print(f"ADVERTENCIA: Subproducto con código '{codigo_sub}' no encontrado para el precio. Saltando.")
                continue

        # Asegurar que cantidad_minima_kg tenga un valor si no está presente
        precio_data_db.setdefault('cantidad_minima_kg', 0.0)

        # Verificar si el precio ya existe usando las UniqueConstraints
        existing_precio = None
        if precio_data_db.get('producto_id'):
            existing_precio = Precio.query.filter_by(
                producto_id=precio_data_db['producto_id'],
                tipo_cliente=precio_data_db['tipo_cliente'],
                cantidad_minima_kg=precio_data_db['cantidad_minima_kg']
            ).first()
        elif precio_data_db.get('subproducto_id'):
             existing_precio = Precio.query.filter_by(
                subproducto_id=precio_data_db['subproducto_id'],
                tipo_cliente=precio_data_db['tipo_cliente'],
                cantidad_minima_kg=precio_data_db['cantidad_minima_kg']
            ).first()

        if not existing_precio:
            precio = Precio(**precio_data_db)
            db.session.add(precio)
        # else:
            # print(f"Precio ya existente para: {precio_data_db}")

    db.session.commit()
    print("Precios poblados.")


@app.cli.command("seed-db")
@with_appcontext
def seed_db_command():
    """Pobla la BD con datos iniciales de catálogo (Modificaciones, Productos, Subproductos, Precios)."""
    # Opción 1: Limpiar datos antes de poblar (CUIDADO CON ESTO EN ENTORNOS QUE NO SEAN DESARROLLO PURO)
    # clear_data()
    # print("Datos de catálogo anteriores eliminados.")

    # Opción 2: No limpiar, las funciones de seed intentarán no duplicar por código/ID.
    #           Esto es más seguro si se ejecuta el comando varias veces.

    seed_modificaciones_data()
    seed_productos_subproductos_data() # Esta función ahora también asocia modificaciones
    seed_precios_data()
    click.echo("Base de datos poblada/actualizada con datos de catálogo.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
