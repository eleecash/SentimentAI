# SentimentAI

SentimentAI es una aplicación web que utiliza inteligencia artificial para analizar el sentimiento de un texto en tiempo real. Este proyecto combina una interfaz de usuario moderna con un backend basado en AWS para ofrecer análisis de sentimientos precisos y rápidos.

## Características

- **Análisis de Sentimientos**: Detecta si un texto es positivo, negativo, neutral o mixto.
- **Historial de Análisis**: Guarda los comentarios analizados para referencia futura.
- **Interfaz Intuitiva**: Diseño limpio y moderno con soporte para dispositivos móviles.
- **Backend Escalable**: Implementado en AWS Lambda y Amazon Comprehend.

## Tecnologías Utilizadas

### Frontend
- **HTML5** y **CSS3**: Para la estructura y el diseño de la interfaz.
- **JavaScript**: Para la lógica del cliente y las interacciones dinámicas.

### Backend
- **AWS Lambda**: Para ejecutar la lógica del análisis de sentimientos.
- **Amazon Comprehend**: Para el análisis de sentimientos basado en IA.
- **DynamoDB**: Para almacenar el historial de análisis (opcional).

### Otros
- **Font Awesome**: Para iconos en la interfaz.
- **Google Fonts**: Para tipografías modernas.

## Estructura del Proyecto

## Configuración

### Requisitos Previos
1. Tener una cuenta de AWS configurada.
2. Crear una tabla en DynamoDB llamada `SentimentAnalysis` con una clave primaria `comment_id`.
3. Configurar las credenciales de AWS en tu entorno local o en Lambda.

### Instalación
1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd SentimentAI
