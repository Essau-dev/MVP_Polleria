document.addEventListener('DOMContentLoaded', function() {
    // Script para cerrar mensajes flash personalizados
    const closeButtons = document.querySelectorAll('.close-message-btn');

    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const messageDiv = button.closest('.message');
            if (messageDiv) {
                messageDiv.style.display = 'none';
            }
        });
    });

    // --- Registro del Service Worker ---
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            // Registra el Service Worker desde la nueva ruta /sw.js
            navigator.serviceWorker.register('/sw.js').then(function(registration) {
                console.log('Service Worker registrado con éxito:', registration.scope);
            }, function(err) {
                console.log('Fallo en el registro del Service Worker:', err);
            });
        });
    } else {
        console.log('Tu navegador no soporta Service Workers.');
    }
    // --- Fin del Registro del Service Worker ---

});