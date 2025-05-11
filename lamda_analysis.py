import json
import boto3
from datetime import datetime
from decimal import Decimal

def lambda_handler(event, context):
    try:
        # 1. Obtener el comentario del cuerpo de la solicitud de manera más robusta
        if isinstance(event, str):
            # Si el evento es un string, parsearlo como JSON
            event = json.loads(event)
        
        # Verificar cómo viene el cuerpo de la solicitud
        if "body" in event:
            if isinstance(event["body"], str):
                body = json.loads(event["body"])
            else:
                body = event["body"]
        else:
            # Si no hay campo body, asumir que el evento mismo es el cuerpo
            body = event
            
        if "comment" not in body:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Campo 'comment' no encontrado en la solicitud"})
            }
            
        comment_text = body["comment"]
        
        if not comment_text.strip():
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "El comentario no puede estar vacío"})
            }

        # 2. Analizar sentimiento con Amazon Comprehend
        comprehend = boto3.client("comprehend")
        sentiment_response = comprehend.detect_sentiment(
            Text=comment_text,
            LanguageCode="es"  # 'en' para inglés
        )
        
        # Convertir valores float a Decimal para posible uso en DynamoDB
        sentiment_scores = {
            "positive": Decimal(str(sentiment_response["SentimentScore"]["Positive"])),
            "negative": Decimal(str(sentiment_response["SentimentScore"]["Negative"])),
            "neutral": Decimal(str(sentiment_response["SentimentScore"]["Neutral"])),
            "mixed": Decimal(str(sentiment_response["SentimentScore"]["Mixed"]))
        }
        
        # 3. Intentar guardar en DynamoDB (pero continuar si hay error)
        try:
            dynamodb = boto3.resource("dynamodb")
            table = dynamodb.Table("SentimentAnalysis")
            
            item = {
                "comment_id": str(datetime.now().timestamp()).replace(".", ""),
                "text": comment_text,
                "sentiment": sentiment_response["Sentiment"],
                "confidence": sentiment_scores,
                "timestamp": datetime.now().isoformat()
            }
            
            table.put_item(Item=item)
        except Exception as db_error:
            # Registrar el error pero continuar sin interrumpir la función
            print(f"Error al guardar en DynamoDB: {str(db_error)}")
            # No necesitamos hacer nada más, simplemente continuamos sin guardar
        
        # 4. Preparar respuesta (independientemente de si se guardó en DynamoDB)
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "sentiment": sentiment_response["Sentiment"],
                "confidence": {
                    "Positive": float(sentiment_scores["positive"]),
                    "Negative": float(sentiment_scores["negative"]),
                    "Neutral": float(sentiment_scores["neutral"]),
                    "Mixed": float(sentiment_scores["mixed"])
                },
                "message": "Análisis completado exitosamente"
            }, default=str)
        }
        
    except KeyError as e:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": f"Campo faltante: '{str(e)}'"})
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Evento recibido: {event}")
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": f"Error interno: {str(e)}"})
        }