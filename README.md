# Pollería Montiel MVP

## Descripción del Proyecto

Este proyecto es una aplicación web Minimal Viable Product (MVP) diseñada para la gestión interna de Pollería Montiel. El objetivo principal es proporcionar una herramienta eficiente para administrar el catálogo de productos, subproductos, modificaciones y precios, así como manejar la autenticación de usuarios.

La aplicación está construida utilizando el microframework Flask, siguiendo una arquitectura modular para facilitar la escalabilidad y el mantenimiento. Se emplean Blueprints para organizar las funcionalidades en módulos lógicos (como autenticación y gestión de productos) y se implementa una capa de servicios (`services.py`) para separar la lógica de negocio de la capa de presentación y acceso a datos.

Además, se están integrando características básicas de Progressive Web App (PWA) para mejorar la experiencia del usuario, incluyendo un archivo manifest y un Service Worker que permite un soporte offline limitado, principalmente para los recursos estáticos cacheables.

## Características Implementadas

Actualmente, el MVP incluye las siguientes funcionalidades clave:

*   **Autenticación de Usuarios:**
    *   **Inicio de Sesión:** Permite a los usuarios registrados acceder a las funcionalidades protegidas de la aplicación. ([`auth.login`](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\auth\routes.py#L12))
    *   **Cierre de Sesión:** Permite a los usuarios cerrar su sesión activa de forma segura. ([`auth.logout`](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\auth\routes.py#L58))
    *   **Gestión Básica de Usuarios:** La estructura de la base de datos y los modelos (`User`) están definidos para soportar la gestión de usuarios, aunque las interfaces de administración de usuarios aún están en desarrollo.

*   **Gestión de Productos:**
    *   **Listado de Productos:** Muestra una lista paginada de todos los productos disponibles en el catálogo. ([`productos.listar_productos`](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\productos\routes.py#L15))
    *   **Creación de Productos:** Permite añadir nuevos productos al catálogo con sus detalles básicos. ([`productos.crear_producto`](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\productos\routes.py#L30))
    *   **Edición de Productos:** Permite modificar la información de productos existentes. ([`productos.editar_producto`](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\productos\routes.py#L51))
    *   **Visualización de Detalles de Producto:** Muestra la información detallada de un producto específico, incluyendo los subproductos y modificaciones que se le pueden aplicar. ([`productos.ver_producto`](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\productos\routes.py#L90))

*   **Gestión de Subproductos:**
    *   **Creación de Subproductos:** Permite añadir subproductos que están asociados a un producto principal (ej: diferentes tamaños o variantes de un producto). ([`productos.crear_subproducto`](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\productos\routes.py#L114))
    *   **Edición de Subproductos:** Permite modificar los detalles de subproductos existentes. ([`productos.editar_subproducto`](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\productos\routes.py#L140))

*   **Gestión de Modificaciones:**
    *   **Listado de Modificaciones:** Muestra una lista de las modificaciones disponibles que se pueden aplicar a productos o subproductos (ej: "sin cebolla", "extra picante"). ([`productos.listar_modificaciones`](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\productos\routes.py#L166))
    *   **Creación de Modificaciones:** Permite añadir nuevas opciones de modificación al sistema. ([`productos.crear_modificacion`](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\productos\routes.py#L179))
    *   **Edición de Modificaciones:** Permite modificar los detalles de modificaciones existentes. ([`productos.editar_modificacion`](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\productos\routes.py#L201))

*   **Arquitectura y Estructura del Código:**
    *   **Blueprints:** La aplicación utiliza Blueprints de Flask para organizar el código en módulos (`auth`, `productos`), mejorando la modularidad y facilitando la gestión de rutas y vistas.
    *   **Capa de Servicios:** Se ha implementado una capa de servicios (`services.py`) para separar la lógica de negocio y las interacciones con la base de datos de las rutas y vistas de Flask, promoviendo un diseño más limpio y mantenible.
    *   **WTForms:** Se utilizan formularios WTForms para manejar la validación y el procesamiento de la entrada del usuario de manera segura y eficiente.
    *   **Jinja2:** Las plantillas HTML se gestionan con Jinja2, aprovechando la herencia de plantillas (`base.html`) y la inclusión de parciales (`_flash_messages.html`) para reutilizar código y mantener la consistencia visual.
    *   **Estilos CSS:** Se utilizan estilos CSS personalizados ([estilo.css](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\static\css\estilo.css)) con variables CSS para facilitar la personalización y un diseño responsive básico para adaptarse a diferentes tamaños de pantalla.

*   **PWA Básica:**
    *   **Archivo Manifest:** Incluye un archivo `manifest.json` ([manifest.json](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\static\manifest.json)) que proporciona metadatos sobre la aplicación, permitiendo que sea añadida a la pantalla de inicio de dispositivos móviles y se comporte más como una aplicación nativa.
    *   **Service Worker:** Se ha implementado un Service Worker (`sw.js`) ([sw.js](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\app\sw.js)) con una estrategia de caché "Network-first" para las páginas HTML (intentar obtener de la red primero, caer a caché si falla) y "Cache-first" para los recursos estáticos (servir desde caché si está disponible, ir a la red si no), lo que permite el acceso offline a los recursos previamente cacheables.

*   **Base de Datos:**
    *   **SQLite:** La aplicación utiliza SQLite como base de datos ligera y fácil de configurar (`app.db`).
    *   **Flask-SQLAlchemy y Flask-Migrate:** Se utiliza Flask-SQLAlchemy como Object-Relational Mapper (ORM) para interactuar con la base de datos de manera orientada a objetos, y Flask-Migrate (basado en Alembic) para gestionar las migraciones de la base de datos, permitiendo evolucionar el esquema de la base de datos de forma controlada.

## Tecnologías Utilizadas

Este proyecto se ha desarrollado utilizando las siguientes tecnologías y bibliotecas principales:

*   **Python:** Lenguaje de programación principal.
*   **Flask:** Microframework web para Python.
*   **Flask-SQLAlchemy:** Extensión de Flask para integrar SQLAlchemy (ORM).
*   **Flask-Migrate (Alembic):** Extensión de Flask para manejar migraciones de base de datos.
*   **Flask-Login:** Extensión de Flask para gestionar sesiones de usuario.
*   **Flask-Moment:** Extensión de Flask para trabajar con fechas y horas en plantillas Jinja2.
*   **WTForms:** Biblioteca para crear y validar formularios web.
*   **Jinja2:** Motor de plantillas para Python.
*   **SQLite:** Base de datos relacional ligera.
*   **HTML5, CSS3, JavaScript:** Tecnologías front-end estándar.

(Basado en [requirements.txt](c:\Users\Essau\Desktop\Proyectos\MVP\MVP_Polleria\requirements.txt))

## Configuración y Ejecución

1.  Clona el repositorio.
2.  Crea un entorno virtual e instálalo:
    ```bash
    python -m venv venv
    venv\Scripts\activate   # En Windows
    # source venv/bin/activate # En macOS/Linux
    ```
3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configura las variables de entorno (por ejemplo, en un archivo `.env` si usas `python-dotenv`):
    *   `SECRET_KEY` (clave secreta para Flask)
    *   `SQLALCHEMY_DATABASE_URI` (ej: `sqlite:///app.db`)
5.  Inicializa y aplica las migraciones de la base de datos:
    ```bash
    flask db upgrade
    ```
6.  (Opcional) Si tienes scripts de seeding, puedes ejecutarlos (ej: `flask seed-data`).
7.  Ejecuta la aplicación:
    ```bash
    flask run
    ```
    La aplicación estará disponible en `http://127.0.0.1:5000/`.

## Próximos Pasos

*   Implementar la gestión completa de Precios (formularios, servicios, rutas, plantillas).
*   Añadir funcionalidades de eliminación para Productos, Subproductos y Modificaciones.
*   Mejorar la interfaz de usuario y la experiencia de usuario (UX).
*   Implementar la gestión de usuarios (registro, edición, roles más detallados).
*   Añadir funcionalidades de ventas/pedidos.
*   Mejorar el soporte offline y la estrategia de caché del Service Worker.
*   Implementar pruebas unitarias y de integración.
