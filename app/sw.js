// Nombre de la caché. Se recomienda versionar el nombre.
const CACHE_NAME = 'polleria-mvp-cache-v3'; // Incrementa la versión para forzar la actualización

// Lista de archivos esenciales que forman el "app shell"
// Estos archivos se cachearán durante la instalación del Service Worker
const urlsToCache = [
    // '/', // Eliminar la página de inicio de la caché inicial si usas Network-first para HTML
    // '/dashboard', // Eliminar páginas HTML de la caché inicial
    // '/auth/login', // Eliminar páginas HTML de la caché inicial
    '/static/css/estilo.css',
    '/static/js/main.js',
    '/static/img/logo.png', // Tu logo principal si se usa directamente
    '/static/img/logo-48x48.png', // Iconos del manifest
    '/static/img/logo-72x72.png',
    '/static/img/logo-96x96.png',
    '/static/img/logo-144x144.png',
    '/static/img/logo-168x168.png',
    '/static/img/logo-192x192.png',
    '/static/img/logo-512x512.png',
    // Añadir recursos externos que son parte del app shell visual
    'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment-with-locales.min.js',
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap',
    // Si tienes una página offline, añádela aquí:
    // '/offline.html',
];

// Evento 'install': Se dispara cuando el Service Worker se instala por primera vez.
// Aquí cacheamos los recursos del "app shell".
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Instalando Service Worker...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[Service Worker] Cacheando app shell');
                // cache.addAll() intenta cachear todos los recursos en la lista.
                // Si falla alguno, la instalación del SW fallará.
                return cache.addAll(urlsToCache);
            })
            .catch((error) => {
                console.error('[Service Worker] Error al cachear app shell:', error);
                // Considera qué hacer si falla la instalación (ej. no activar el SW)
                // throw error; // Lanzar el error puede evitar que el SW se active si la caché inicial es crítica
            })
    );
});

// Evento 'activate': Se dispara cuando el Service Worker se activa.
// Aquí limpiamos cachés antiguas.
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Activando Service Worker...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    // Elimina cachés que no coinciden con el CACHE_NAME actual
                    if (cacheName !== CACHE_NAME) {
                        console.log('[Service Worker] Eliminando caché antigua:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Evento 'fetch': Se dispara cada vez que el navegador intenta obtener un recurso.
// Aquí interceptamos las solicitudes y decidimos cómo responder (desde caché o red).
self.addEventListener('fetch', (event) => {
    // console.log('[Service Worker] Interceptando fetch:', event.request.url);

    // Estrategia para solicitudes de navegación (HTML): Network-first, luego cache
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request)
                .then((networkResponse) => {
                    // Si la solicitud de red es exitosa, devuelve la respuesta de red
                    // Opcional: Cachear la respuesta de red para usarla como fallback offline
                    if (networkResponse.status === 200) {
                         const responseToCache = networkResponse.clone();
                         caches.open(CACHE_NAME).then((cache) => {
                             cache.put(event.request, responseToCache);
                             // console.log('[Service Worker] Cacheado recurso de red para fallback:', event.request.url);
                         });
                    }
                    return networkResponse;
                })
                .catch((error) => {
                    // Si la solicitud de red falla (ej. offline), intenta responder desde la caché
                    console.error('[Service Worker] Fetch de navegación falló, intentando caché:', event.request.url, error);
                    return caches.match(event.request).then(cachedResponse => {
                        if (cachedResponse) {
                            // console.log('[Service Worker] Sirviendo fallback desde caché:', event.request.url);
                            return cachedResponse;
                        }
                        // Si no hay versión cacheada, intenta servir una página offline genérica
                        return caches.match('/offline.html').then(offlineResponse => {
                            if (offlineResponse) {
                                console.log('[Service Worker] Sirviendo página offline.');
                                return offlineResponse;
                            }
                            // Si no hay página offline cacheada, devuelve una respuesta de error
                            return new Response('<h1>Offline</h1><p>No estás conectado y la página no está disponible offline.</p>', {
                                headers: { 'Content-Type': 'text/html' }
                            });
                        });
                    });
                })
        );
    } else {
        // Estrategia para otros recursos (CSS, JS, imágenes, etc.): Cache-first, luego network
        event.respondWith(
            caches.match(event.request)
                .then((response) => {
                    // Si el recurso está en caché, responde con la versión cacheada
                    if (response) {
                        // console.log('[Service Worker] Sirviendo desde caché:', event.request.url);
                        return response;
                    }

                    // Si el recurso NO está en caché, intenta obtenerlo de la red
                    console.log('[Service Worker] Recurso no encontrado en caché, yendo a la red:', event.request.url);
                    return fetch(event.request)
                        .then((networkResponse) => {
                            // Cachear nuevas respuestas de la red para futuras visitas
                            if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
                                return networkResponse;
                            }

                            const responseToCache = networkResponse.clone();

                            caches.open(CACHE_NAME).then((cache) => {
                                cache.put(event.request, responseToCache);
                                // console.log('[Service Worker] Cacheado recurso de red:', event.request.url);
                            });

                            return networkResponse;
                        })
                        .catch((error) => {
                            // Esto se ejecuta si la solicitud de red falla (ej. offline)
                            console.error('[Service Worker] Fetch de recurso falló:', event.request.url, error);
                            // Aquí podrías manejar fallos específicos para otros tipos de recursos si es necesario
                            throw error; // O devuelve una respuesta de fallback específica para el tipo de recurso
                        });
                })
        );
    }
});

// Puedes añadir más eventos y estrategias de caché según necesites
// (ej. network-first para APIs, stale-while-revalidate para recursos que cambian a menudo)