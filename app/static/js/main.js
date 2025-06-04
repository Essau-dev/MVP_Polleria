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

    // --- Lógica para el Generador de Descripción de Producto con Gemini API ---
    const generateDescriptionBtn = document.getElementById('generateDescriptionBtn');
    const productNameInput = document.getElementById('productName');
    const productDescriptionInput = document.getElementById('productDescription');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const generatedDescriptionContainer = document.getElementById('generatedDescriptionContainer');
    const generatedDescriptionTextarea = document.getElementById('generatedDescription');
    const applyGeneratedDescriptionBtn = document.getElementById('applyGeneratedDescriptionBtn');

    if (generateDescriptionBtn && productNameInput && productDescriptionInput) {
        generateDescriptionBtn.addEventListener('click', async () => {
            const productName = productNameInput.value.trim();
            const currentDescription = productDescriptionInput.value.trim();

            if (!productName) {
                // Usamos un mensaje de error simple, ya que no tenemos un sistema de notificación global en JS
                // Idealmente, se mostraría un mensaje flash o una alerta modal personalizada.
                alert('Por favor, ingresa el nombre del producto antes de generar una descripción.');
                return;
            }

            // Mostrar indicador de carga
            loadingIndicator.style.display = 'block';
            generateDescriptionBtn.disabled = true; // Deshabilitar botón durante la carga
            generatedDescriptionContainer.style.display = 'none'; // Ocultar resultados anteriores

            try {
                let chatHistory = [];
                const prompt = `Eres un especialista en cortes y descripciones de productos de pollería. Redacta una descripción clara, atractiva y detallada para una modificación del producto.
                                El nombre del producto es '${productName}'.
                                La descripción actual es '${currentDescription}'.
                                Si la descripción actual es corta o genérica, mejórala haciéndola más útil para el cliente.
                                Si no hay descripción actual, crea una desde cero.
                                Resalta la frescura, calidad y posibles usos culinarios.
                                Limita la descripción a 100-150 palabras.
                                Asegúrate de que la respuesta sea solo la descripción, sin introducciones ni conclusiones.`;

                chatHistory.push({ role: "user", parts: [{ text: prompt }] });

                const payload = { contents: chatHistory };
                // IMPORTANTE: Si estás ejecutando esto localmente, DEBES pegar tu clave API aquí.
                // Si estás en el entorno de Canvas, déjalo como ""
                const apiKey = "AIzaSyB05MIGXH7vOTF3pFmBlauD7oTXqv-Sm1I"; // <-- PEGA TU CLAVE API REAL AQUÍ PARA DESARROLLO LOCAL
                const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                // Verificar si la respuesta fue exitosa (código 2xx)
                if (!response.ok) {
                    const errorData = await response.json();
                    console.error('Error de la API de Gemini:', response.status, errorData);
                    alert(`Error al generar la descripción: ${errorData.error.message || 'Error desconocido'}. Código: ${response.status}. Por favor, verifica tu clave API y sus restricciones.`);
                    return; // Salir de la función si hay un error HTTP
                }

                const result = await response.json();

                if (result.candidates && result.candidates.length > 0 &&
                    result.candidates[0].content && result.candidates[0].content.parts &&
                    result.candidates[0].content.parts.length > 0) {
                    const generatedText = result.candidates[0].content.parts[0].text;
                    generatedDescriptionTextarea.value = generatedText;
                    generatedDescriptionContainer.style.display = 'block'; // Mostrar el área de texto generada
                } else {
                    console.error('Estructura de respuesta inesperada de la API de Gemini:', result);
                    alert('No se pudo generar la descripción. La respuesta de la API fue inesperada. Inténtalo de nuevo más tarde.');
                }
            } catch (error) {
                console.error('Error al llamar a la API de Gemini:', error);
                alert('Ocurrió un error de red o al procesar la respuesta de la API. Por favor, verifica tu conexión o inténtalo más tarde.');
            } finally {
                // Ocultar indicador de carga y habilitar botón
                loadingIndicator.style.display = 'none';
                generateDescriptionBtn.disabled = false;
            }
        });

        // Lógica para aplicar la descripción generada al campo principal
        if (applyGeneratedDescriptionBtn && productDescriptionInput && generatedDescriptionTextarea) {
            applyGeneratedDescriptionBtn.addEventListener('click', () => {
                productDescriptionInput.value = generatedDescriptionTextarea.value;
                // Opcional: Ocultar el contenedor de la descripción generada después de aplicarla
                generatedDescriptionContainer.style.display = 'none';
            });
        }
    }

    // --- Lógica para el Generador de Descripción de Modificación con Gemini API ---
    const generateModificacionDescriptionBtn = document.getElementById('generateModificacionDescriptionBtn');
    const modificacionNameInput = document.getElementById('modificacionName');
    const modificacionDescriptionInput = document.getElementById('modificacionDescription');
    const loadingModificacionIndicator = document.getElementById('loadingModificacionIndicator');
    const generatedModificacionDescriptionContainer = document.getElementById('generatedModificacionDescriptionContainer');
    const generatedModificacionDescriptionTextarea = document.getElementById('generatedModificacionDescription');
    const applyGeneratedModificacionDescriptionBtn = document.getElementById('applyGeneratedModificacionDescriptionBtn');

    if (generateModificacionDescriptionBtn && modificacionNameInput && modificacionDescriptionInput) {
        generateModificacionDescriptionBtn.addEventListener('click', async () => {
            const modificacionName = modificacionNameInput.value.trim();
            const currentModificacionDescription = modificacionDescriptionInput.value.trim();

            if (!modificacionName) {
                alert('Por favor, ingresa el nombre de la modificación antes de generar una descripción.');
                return;
            }

            // Mostrar indicador de carga
            loadingModificacionIndicator.style.display = 'block';
            generateModificacionDescriptionBtn.disabled = true;
            generatedModificacionDescriptionContainer.style.display = 'none';

            try {
                let chatHistory = [];
                const prompt = `Eres un especialista en cortes y descripciones de productos de pollería. Redacta una descripción clara, atractiva y detallada para una modificación del producto. 
                                El nombre de la modificación es '${modificacionName}'.
                                La descripción actual es '${currentModificacionDescription}'.
                                Si la descripción actual es corta o genérica, mejórala haciéndola más útil para el cliente.
                                Si no hay descripción actual, crea una desde cero.
                                Enfócate en cómo esta modificación afecta el producto original (ej. tipo de corte, si incluye o no ciertas partes, etc.).
                                Limita la descripción a 25 -40 palabras.
                                Asegúrate de que la respuesta sea solo la descripción, sin introducciones, ni conclusiones.`;

                chatHistory.push({ role: "user", parts: [{ text: prompt }] });

                const payload = { contents: chatHistory };
                // IMPORTANTE: Si estás ejecutando esto localmente, DEBES pegar tu clave API aquí.
                // Si estás en el entorno de Canvas, déjalo como ""
                const apiKey = "AIzaSyB05MIGXH7vOTF3pFmBlauD7oTXqv-Sm1I"; // <-- PEGA TU CLAVE API REAL AQUÍ PARA DESARROLLO LOCAL
                const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                // Verificar si la respuesta fue exitosa (código 2xx)
                if (!response.ok) {
                    const errorData = await response.json();
                    console.error('Error de la API de Gemini para modificación:', response.status, errorData);
                    alert(`Error al generar la descripción de la modificación: ${errorData.error.message || 'Error desconocido'}. Código: ${response.status}. Por favor, verifica tu clave API y sus restricciones.`);
                    return; // Salir de la función si hay un error HTTP
                }

                const result = await response.json();

                if (result.candidates && result.candidates.length > 0 &&
                    result.candidates[0].content && result.candidates[0].content.parts &&
                    result.candidates[0].content.parts.length > 0) {
                    const generatedText = result.candidates[0].content.parts[0].text;
                    generatedModificacionDescriptionTextarea.value = generatedText;
                    generatedModificacionDescriptionContainer.style.display = 'block';
                } else {
                    console.error('Estructura de respuesta inesperada de la API de Gemini para modificación:', result);
                    alert('No se pudo generar la descripción de la modificación. La respuesta de la API fue inesperada. Inténtalo de nuevo más tarde.');
                }
            } catch (error) {
                console.error('Error al llamar a la API de Gemini para modificación:', error);
                alert('Ocurrió un error de red o al procesar la respuesta de la API. Por favor, verifica tu conexión o inténtalo más tarde.');
            } finally {
                loadingModificacionIndicator.style.display = 'none';
                generateModificacionDescriptionBtn.disabled = false;
            }
        });

        if (applyGeneratedModificacionDescriptionBtn && modificacionDescriptionInput && generatedModificacionDescriptionTextarea) {
            applyGeneratedModificacionDescriptionBtn.addEventListener('click', () => {
                modificacionDescriptionInput.value = generatedModificacionDescriptionTextarea.value;
                generatedModificacionDescriptionContainer.style.display = 'none';
            });
        }
    }
});
