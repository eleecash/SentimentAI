async function analyzeSentiment() {
    const comment = document.getElementById('comment').value.trim();
    const resultDiv = document.getElementById('result');
    const historyDiv = document.getElementById('history');

    if (!comment) {
        alert("Por favor escribe un comentario");
        return;
    }

    try {
        // Mostrar loader
        resultDiv.innerHTML = '<div class="loader"></div>';
        const API_URL = 'https://51i28dt9l0.execute-api.us-east-1.amazonaws.com/prod/analyze';

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ comment: comment })
        });

        // Parsear la respuesta como JSON
        const data = await response.json();
        console.log('Respuesta de API:', data); // Para inspeccionar la estructura real de la respuesta
        
        // Intentar extraer el mensaje o sentimiento de diferentes posibles estructuras
        let message;
        
        if (typeof data === 'string') {
            // Si la API devuelve directamente un string
            message = data;
        } else if (data && typeof data === 'object') {
            // Si devuelve statusCode y body (estructura actual)
            if (data.statusCode === 200 && data.body) {
                try {
                    // El body puede ser un string JSON que necesita ser parseado
                    const parsedBody = typeof data.body === 'string' ? JSON.parse(data.body) : data.body;
                    
                    // Extraer el sentimiento del objeto parseado
                    if (parsedBody.sentiment) {
                        let sentimentText = parsedBody.sentiment;
                        
                        // Traducir el sentimiento al español
                        if (sentimentText === 'POSITIVE') sentimentText = 'POSITIVO';
                        else if (sentimentText === 'NEGATIVE') sentimentText = 'NEGATIVO';
                        else if (sentimentText === 'NEUTRAL') sentimentText = 'NEUTRAL';
                        else if (sentimentText === 'MIXED') sentimentText = 'MIXTO';
                        
                        message = `Sentimiento: ${sentimentText}`;
                    } else if (parsedBody.message) {
                        message = parsedBody.message;
                    } else if (typeof parsedBody === 'string') {
                        message = parsedBody;
                    } else {
                        message = "Análisis completado";
                    }
                } catch (e) {
                    message = data.body;
                }
            } else {
                // Intentar otras ubicaciones posibles del mensaje o sentimiento
                message = data.sentiment || 
                        data.message ||
                        (data.body && data.body.sentiment) ||
                        null;
            }
        }
        
        // Verificar si se obtuvo un mensaje válido
        if (!message) {
            resultDiv.innerHTML = '❌ No se pudo obtener respuesta del servidor';
            console.error('No se pudo extraer ningún mensaje de la respuesta:', data);
            return;
        }

        // Mostrar resultado (temporalmente sin aplicar clases de sentimiento)
        resultDiv.innerHTML = `<span>${message}</span>`;

        // Añadir al historial (temporalmente sin aplicar clases de sentimiento)
        historyDiv.innerHTML = `
            <div class="history-item">
                <p>"${comment}"</p>
                <span>${message}</span>
            </div>
            ${historyDiv.innerHTML}
        `;

    } catch (error) {
        resultDiv.innerHTML = '❌ Error al analizar el comentario';
        console.error('Error en analyzeSentiment:', error);
    }
}